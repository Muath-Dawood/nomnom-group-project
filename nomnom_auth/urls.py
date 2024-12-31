from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import LoginView, SignupView

urlpatterns = [
    path('register/', SignupView.as_view(), name='auth_register'),
    path('login/', LoginView.as_view(), name='auth_login'),
    path('logout/', LogoutView.as_view(next_page='auth_login'), name='auth_logout'),
]
