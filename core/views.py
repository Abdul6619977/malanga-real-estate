import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Q
from django.contrib.auth.decorators import login_required
from .models import Property, Inquiry, PropertyImage

# ─── PUBLIC STOREFRONT VIEWS ──────────────────────────────────────────────────

def public_home(request):
    """Luxury property gallery for potential buyers with filtering."""
    location_query = request.GET.get('location')
    type_query = request.GET.get('type')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    bedrooms = request.GET.get('bedrooms')
    
    properties = Property.objects.filter(status='Available').order_by('-created_at')
    
    if location_query and location_query != 'all':
        properties = properties.filter(location__icontains=location_query)
        
    if type_query and type_query != 'all':
        properties = properties.filter(property_type=type_query)
        
    if min_price:
        try:
            properties = properties.filter(price__gte=min_price)
        except (ValueError, TypeError):
            pass

    if max_price:
        try:
            properties = properties.filter(price__lte=max_price)
        except (ValueError, TypeError):
            pass

    if bedrooms and bedrooms != 'any':
        try:
            properties = properties.filter(bedrooms__gte=bedrooms)
        except (ValueError, TypeError):
            pass
            
    return render(request, 'core/public_home.html', {
        'properties': properties,
        'current_location': location_query,
        'current_type': type_query,
        'min_price': min_price,
        'max_price': max_price,
        'current_bedrooms': bedrooms
    })

def public_detail(request, pk):
    """Detailed showcase of a property with enquiry form and gallery."""
    property = get_object_or_404(Property, pk=pk)
    images = property.images.all()
    return render(request, 'core/public_detail.html', {
        'property': property,
        'images': images
    })

def submit_inquiry(request):
    """Handles inquiry form submissions from potential buyers."""
    if request.method == 'POST':
        property_id = request.POST.get('property_id')
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        property = get_object_or_404(Property, id=property_id)
        Inquiry.objects.create(
            property=property,
            customer_name=name,
            customer_email=email,
            message=message
        )
        messages.success(request, f"Thank you {name}, your inquiry for '{property.name}' has been sent!")
        return redirect('public_detail', pk=property.id)
    return redirect('public_home')


# ─── MANAGEMENT DASHBOARD (AUTHENTICATED) ───────────────────────────────────

@login_required
def dashboard(request):
    """Refined Sales-Only Dashboard with Advanced Analytics."""
    total_inventory_value = Property.objects.filter(status='Available').aggregate(Sum('price'))['price__sum'] or 0
    realized_revenue = Property.objects.filter(status='Sold').aggregate(Sum('price'))['price__sum'] or 0
    
    total_properties = Property.objects.count()
    sold_properties = Property.objects.filter(status='Sold').count()
    total_inquiries = Inquiry.objects.count()
    
    # Conversion Rate
    conversion_rate = 0
    if total_inquiries > 0:
        conversion_rate = round((sold_properties / total_inquiries) * 100, 1)

    new_inquiries = Inquiry.objects.all().order_by('-created_at')[:5]
    
    # ─── Chart Data ───────────────────────────────────────────────────────────
    # Inquiry Distribution (Top 5 Properties)
    from django.db.models import Count
    prop_leads = Property.objects.annotate(lead_count=Count('inquiries')).order_by('-lead_count')[:5]
    chart_labels = [p.name for p in prop_leads]
    chart_data = [p.lead_count for p in prop_leads]
    
    return render(request, 'core/manage/dashboard.html', {
        'total_inventory_value': total_inventory_value,
        'realized_revenue': realized_revenue,
        'total_properties': total_properties,
        'sold_properties': sold_properties,
        'total_inquiries': total_inquiries,
        'conversion_rate': conversion_rate,
        'new_inquiries': new_inquiries,
        'chart_labels': chart_labels,
        'chart_data': chart_data
    })

@login_required
def update_inquiry_status(request, pk):
    """Update lead status from the inquiries management page."""
    inquiry = get_object_or_404(Inquiry, pk=pk)
    if request.method == 'POST':
        status = request.POST.get('status')
        inquiry.status = status
        inquiry.save()
        messages.success(request, f"Lead for '{inquiry.property.name}' updated to {status}!")
    return redirect('inquiries')

@login_required
def properties_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        property_type = request.POST.get('property_type', 'House')
        location = request.POST.get('location')
        price = request.POST.get('price')
        bedrooms = request.POST.get('bedrooms')
        bathrooms = request.POST.get('bathrooms')
        size_sqm = request.POST.get('size_sqm')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        gallery_images = request.FILES.getlist('gallery_images')
        
        # Convert empty strings to None for integer fields
        bedrooms = int(bedrooms) if bedrooms else None
        bathrooms = int(bathrooms) if bathrooms else None
        size_sqm = int(size_sqm) if size_sqm else None
        
        property = Property.objects.create(
            name=name, 
            property_type=property_type,
            location=location, 
            price=price,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            size_sqm=size_sqm,
            description=description,
            image=image
        )

        # Save Gallery Images
        for img in gallery_images:
            PropertyImage.objects.create(property=property, image=img)

        messages.success(request, f"Property '{name}' listing created successfully with {len(gallery_images)} gallery images.")
        return redirect('properties')
    
    properties = Property.objects.all().order_by('-created_at')
    return render(request, 'core/manage/properties.html', {'properties': properties})

@login_required
def update_property_status(request, pk, new_status):
    """Dynamic status update for property listings."""
    property = get_object_or_404(Property, pk=pk)
    # Choices are [('Pending', 'Pending'), ('Available', 'Available'), ...]
    valid_statuses = [s[0] for s in Property.STATUS_CHOICES]
    
    if new_status in valid_statuses:
        old_status = property.status
        property.status = new_status
        property.save()
        messages.success(request, f"Property '{property.name}' status updated to {new_status}!")
    else:
        messages.error(request, f"Invalid status selection: {new_status}")
        
    return redirect('properties')

@login_required
def inquiries_page(request):
    inquiries = Inquiry.objects.all().order_by('-created_at')
    return render(request, 'core/manage/inquiries.html', {'inquiries': inquiries})

@login_required
def settings_page(request):
    """Manage Admin settings and Provision Team Accounts"""
    from django.contrib.auth.models import User
    from django.contrib.auth import update_session_auth_hash

    if request.method == 'POST':
        action = request.POST.get('action')
        
        # 1. Update Personal Username
        if action == 'update_username':
            new_username = request.POST.get('username')
            if new_username and not User.objects.filter(username=new_username).exclude(pk=request.user.pk).exists():
                request.user.username = new_username
                request.user.save()
                messages.success(request, "Your master username has been updated!")
            else:
                messages.error(request, "That username is already taken or invalid.")
        
        # 2. Update Personal Password
        elif action == 'update_password':
            new_pass = request.POST.get('new_password')
            confirm_pass = request.POST.get('confirm_password')
            if new_pass == confirm_pass and len(new_pass) > 2:
                request.user.set_password(new_pass)
                request.user.save()
                update_session_auth_hash(request, request.user) # Keeps user logged in
                messages.success(request, "Your master password has been completely secured.")
            else:
                messages.error(request, "Passwords did not match.")
                
        # 3. Create Staff Account
        elif action == 'create_staff':
            staff_username = request.POST.get('staff_username')
            staff_pass = request.POST.get('staff_password')
            if staff_username and staff_pass and not User.objects.filter(username=staff_username).exists():
                user = User.objects.create_user(username=staff_username, password=staff_pass)
                # By default they can just log in. They don't need 'is_staff=True' unless using django's built in /admin/
                messages.success(request, f"New team member '{staff_username}' has been granted access!")
            else:
                messages.error(request, "Failed to create team member. Username may already exist.")
                
        return redirect('settings')
        
    staff_members = User.objects.all().exclude(pk=request.user.pk)
    return render(request, 'core/manage/settings.html', {'staff_members': staff_members})

@login_required
def delete_inquiry(request, pk):
    inquiry = get_object_or_404(Inquiry, pk=pk)
    inquiry.delete()
    messages.success(request, "Lead inquiry has been removed.")
    return redirect('inquiries')

@login_required
def delete_property(request, pk):
    property = get_object_or_404(Property, pk=pk)
    
    # 1. Delete main image file from disk
    if property.image:
        if os.path.isfile(property.image.path):
            os.remove(property.image.path)
            
    # 2. Delete gallery image files from disk
    for g_img in property.images.all():
        if os.path.isfile(g_img.image.path):
            os.remove(g_img.image.path)
            
    name = property.name
    property.delete()
    messages.success(request, f"Property '{name}' and all media records have been permanently cleared.")
    return redirect('properties')

@login_required
def edit_property(request, pk):
    property = get_object_or_404(Property, pk=pk)
    
    if request.method == 'POST':
        property.name = request.POST.get('name')
        property.property_type = request.POST.get('property_type')
        property.location = request.POST.get('location')
        property.price = request.POST.get('price')
        property.bedrooms = int(request.POST.get('bedrooms')) if request.POST.get('bedrooms') else None
        property.bathrooms = int(request.POST.get('bathrooms')) if request.POST.get('bathrooms') else None
        property.size_sqm = int(request.POST.get('size_sqm')) if request.POST.get('size_sqm') else None
        property.description = request.POST.get('description')
        property.status = request.POST.get('status')
        
        if request.FILES.get('image'):
            property.image = request.FILES.get('image')
            
        property.save()
        
        # New Gallery Images
        gallery_images = request.FILES.getlist('gallery_images')
        for img in gallery_images:
            PropertyImage.objects.create(property=property, image=img)
            
        messages.success(request, f"Property '{property.name}' has been successfully updated.")
        return redirect('properties')
        
def debug_auth(request):
    """Temporary diagnostic view to debug live authentication issues."""
    import os
    from django.contrib.auth.models import User
    from django.http import HttpResponse

    username_env = os.environ.get('ADMIN_USERNAME', 'NOT SET')
    password_env = 'SET (HIDDEN)' if os.environ.get('ADMIN_PASSWORD') else 'NOT SET'
    
    user_exists = User.objects.filter(username=username_env).exists() if username_env != 'NOT SET' else False
    all_users = list(User.objects.all().values_list('username', flat=True))
    
    html = f"""
    <h1>Live Auth Diagnostic</h1>
    <p><b>ADMIN_USERNAME (Env):</b> {username_env}</p>
    <p><b>ADMIN_PASSWORD (Env):</b> {password_env}</p>
    <p><b>Does user "{username_env}" exist in DB?</b> {'YES' if user_exists else 'NO'}</p>
    <p><b>All Existing Users in DB:</b> {all_users}</p>
    <hr>
    <p>If the user doesn't exist, check your Render Environment variables to ensure they are saved correctly.</p>
    """
    return HttpResponse(html)
