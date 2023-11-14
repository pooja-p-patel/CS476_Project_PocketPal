from django.contrib import admin
# add admin
from django.urls import path, include
# import path and include from django.urls
from django.views.generic import TemplateView
# import Templateview
from . import views
# import views from django.views
# from django.conf import settings
# from django.conf.urls.static import static


# added url path
urlpatterns = [
    # url path to show index page
    path('', TemplateView.as_view(template_name="index.html"),name="index"),
    # url path to add admin urls
    path('admin/', admin.site.urls),
    # url path to show student user dashboard
    path('dashboard/',views.dashboard,name="dashboard"),
    # url path to show student data analytics to admin/advisor
    path('view-dashboard/<int:pk>',views.view_dashboard,name="view_dashboard"),
    # url path to include expense app
    path('expense/', include('Expense.urls')),
    # url path to inculde user authentication app
    path('auth/user/', include('user.urls')),
    # url path to include income app
    path('income/', include('Income.urls')),
    # url path to include advisor app
    path('advisor/', include('advisor.urls')),
    # url path to include advice app
    path('advise/', include('advise.urls')),
]


# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root = settings.STATICFILES_DIRS)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
