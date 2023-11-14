from django.urls import path
# import path from django.urls
from . import views, api
# from the current directory import views.py and api.py 


# added url path
urlpatterns = [
    # url path to view expenses
    path('view/', views.expense_page, name = 'expense_page'),
    # url path to add expenses
    path('add-expense/', views.add_expense, name = 'add_expense'),
    # url path to delete expenses
    path('delete-expense/<int:id>/', views.delete_expense, name = 'delete_expense'),
    # url path to edit expenses
    path('edit-expense/<int:id>/',views.edit_expense,name="edit_expense"),
    # api call to show expense data on student dashboard using charts
    path('expense-summary-data', api.expense_summary,name="expense_summary_data"),
    # url path to show expense reports categorizing source/account in form of table view
    path('expense-summary/',views.expense_summary,name="expense_summary"),
    # url path to show expense reports categorizing category in form of table view
    path('expense_summary_category/', views.expense_summary_category, name = "expense_summary_category"),
]
