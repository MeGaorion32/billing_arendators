from django.urls import path
from .views import RegisterView, LoginView, LogoutView, UserProfileView, AdminOnlyView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('admin-only/', AdminOnlyView.as_view(), name='admin-only'),
]