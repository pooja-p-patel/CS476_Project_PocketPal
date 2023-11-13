from django.urls import path
# import path from django.urls
from . import views, api
# from the current directory import views.py and api.py 


# added url path
urlpatterns = [
    # url path to view all incomes
    path('view/',views.income_page,name="income"),
    # url path to add income
    path('add-income/',views.add_income,name="add_income"),
    # url path to add income source
    path('add-source/',views.add_income_source,name="add_income_source"),
    # url path to edit income source
    path('edit-source/<int:id>/',views.edit_income_source,name="edit_income_source"),
    # url path to delete income source
    path('delete-income-source/<int:id>/',views.delete_income_source,name="delete_income_source"),
    # url path to edit income
    path('edit-income/<int:id>/',views.edit_income,name="edit_income"),
    # url path to delete income 
    path('delete-income/<int:id>/',views.delete_income,name="delete_income"),
    # api call to show income data in the form of charts
    path('income-summary-data',api.income_summary,name="income_summary_data"),
]