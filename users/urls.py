from django.urls import path
from .views import (admin_dashboard, client_dashboard, renter_dashboard, 
                   create_user, update_user, delete_user)

urlpatterns = [
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('client/dashboard/', client_dashboard, name='client_dashboard'),
    path('renter/dashboard/', renter_dashboard, name='renter_dashboard'),
    path('admin/create-user/', create_user, name='create_user'),
    path('update/<int:pk>/', update_user, name='update_user'),
    path('delete/<int:pk>/', delete_user, name='delete_user'),
]