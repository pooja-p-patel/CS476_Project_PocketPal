from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html"),name="index"),
    path('admin/', admin.site.urls),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('view-dashboard/<int:pk>',views.view_dashboard,name="view_dashboard"),
    path('expense/', include('Expense.urls')),
    path('auth/user/', include('user.urls')),
    path('income/', include('Income.urls')),
    path('advisor/', include('advisor.urls')),
    path('advise/', include('advise.urls')),
]


# path('api/token/', TokenObtainPairView.as_view()),
# path('api/token/refresh/', TokenRefreshView.as_view()),
# path('api/token/verify/', TokenVerifyView.as_view()),