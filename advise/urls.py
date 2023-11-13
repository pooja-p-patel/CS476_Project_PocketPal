from django.urls import path
# import path from django.urls
from . import views
# import views 

# added url path
urlpatterns = [
    # url path for advice opt in
    path('ask-advice/', views.ask_advice, name = 'ask_advice'),
    # url path for checking advice
    path('check-advice/', views.check_advice, name = 'check_advice'),
]