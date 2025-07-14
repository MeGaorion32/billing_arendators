from django.urls import path
from . import views

app_name = 'apartments'

urlpatterns = [
    path('', views.apartments_list, name='apartments_list'),
    path('create/', views.create_apartment, name='create_apartment'),
    path('update/<int:pk>/', views.update_apartment, name='update_apartment'),
    path('delete/<int:pk>/', views.delete_apartment, name='delete_apartment'),
]