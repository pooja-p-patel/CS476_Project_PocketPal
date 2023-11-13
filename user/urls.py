from django.urls import path
from .views import RegistrationView, LoginView, LogoutView, AdminLoginView

urlpatterns = [
    # path('register', RegistrationView.as_view()),
    # path('retrieve', GetUserView.as_view()),
    path('register/',RegistrationView.as_view(),name = 'register'),
    path('login/', LoginView.as_view(), name="login"), 
    path('logout/', LogoutView.as_view(), name="logout"),
    path('admin-login/', AdminLoginView.as_view(), name="admin_login")
]