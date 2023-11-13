from django.urls import path
# import path from django.urls
from .views import RegistrationView, LoginView, LogoutView, AdminLoginView
# import all the classes from Tracker.views.py


# added url path
urlpatterns = [
    # url path to register
    path('register/',RegistrationView.as_view(),name = 'register'),
    # url path to login
    path('login/', LoginView.as_view(), name="login"), 
    # url path to logout
    path('logout/', LogoutView.as_view(), name="logout"),
    # url path to admin login
    path('admin-login/', AdminLoginView.as_view(), name="admin_login")
]