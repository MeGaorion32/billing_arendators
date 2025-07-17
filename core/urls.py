from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users.views import login_view, logout_view, forbidden_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('forbidden/', forbidden_view, name='forbidden'),
    path('users/', include('users.urls')),
    path('apartments/', include('apartments.urls')),
    path('communal_services/', include('communal_services.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)