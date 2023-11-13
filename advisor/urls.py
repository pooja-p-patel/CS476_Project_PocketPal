from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.advisor_dashboard, name = 'advisor_dashboard'),
    path('comment/', views.comment, name = 'comment'),
    path('add-comment/<int:pk>', views.add_comment, name = 'add_comment'),
    path('edit-comment/<int:pk>', views.edit_comment, name = 'edit_comment'),
    path('delete-comment/<int:pk>/', views.delete_comment, name = 'delete_comment'),
]