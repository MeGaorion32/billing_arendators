from django.urls import path
from . import views

app_name = 'communal_services'

urlpatterns = [
    # Коммунальные услуги
    path('', views.service_list, name='service_list'),
    path('service/create/', views.service_create, name='service_create'),
    path('service/<int:pk>/edit/', views.service_edit, name='service_edit'),
    path('service/<int:pk>/delete/', views.service_delete, name='service_delete'),
    
    # Типы коммунальных услуг
    path('service/<int:service_pk>/type/create/', views.service_type_create, name='service_type_create'),
    path('service/<int:service_pk>/type/<int:pk>/edit/', views.service_type_edit, name='service_type_edit'),
    path('service/<int:service_pk>/type/<int:pk>/delete/', views.service_type_delete, name='service_type_delete'),
]