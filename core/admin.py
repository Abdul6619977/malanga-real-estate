from django.contrib import admin
from .models import Property, Inquiry, PropertyImage

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 3

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'price', 'status', 'created_at')
    list_filter = ('status', 'location')
    search_fields = ('name', 'location')
    inlines = [PropertyImageInline]

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'customer_email', 'property', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('customer_name', 'customer_email', 'property__name')
