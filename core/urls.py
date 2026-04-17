from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Public Storefront
    path('', views.public_home, name='public_home'),
    path('property/<int:pk>/', views.public_detail, name='public_detail'),
    path('inquire/', views.submit_inquiry, name='submit_inquiry'),

    # Management (Private Sales Dashboard)
    path('manage/', views.dashboard, name='dashboard'),
    path('manage/properties/', views.properties_page, name='properties'),
    path('manage/properties/<int:pk>/edit/', views.edit_property, name='edit_property'),
    path('manage/properties/<int:pk>/delete/', views.delete_property, name='delete_property'),
    path('manage/properties/<int:pk>/sold/', views.mark_sold, name='mark_sold'),
    path('manage/inquiries/', views.inquiries_page, name='inquiries'),
    path('manage/inquiries/<int:pk>/status/', views.update_inquiry_status, name='update_inquiry_status'),
    path('manage/inquiries/<int:pk>/delete/', views.delete_inquiry, name='delete_inquiry'),
    path('manage/settings/', views.settings_page, name='settings'),
    path('debug-auth/', views.debug_auth, name='debug_auth'),
]
