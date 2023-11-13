from django.urls import path
# import path from django.urls
from . import views
# import views


# added url path
urlpatterns = [
    # url path for displaying admin dashboard
    path('dashboard/', views.advisor_dashboard, name = 'advisor_dashboard'),
    # url path for displaying all comments page
    path('comment/', views.comment, name = 'comment'),
    # url path for adding comment
    path('add-comment/<int:pk>', views.add_comment, name = 'add_comment'),
    # url path for editing comment
    path('edit-comment/<int:pk>', views.edit_comment, name = 'edit_comment'),
    # url path for deleting comment
    path('delete-comment/<int:pk>/', views.delete_comment, name = 'delete_comment'),
]