from django.contrib import admin
from django.urls import path, include
from users.views import login_view, logout_view, forbidden_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('forbidden/', forbidden_view, name='forbidden'),
    path('users/', include('users.urls')),
    path('apartments/', include('apartments.urls')),
]