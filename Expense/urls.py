from django.urls import path
from . import views, api
from django.views.generic import TemplateView

urlpatterns = [
    path('view/', views.expense_page, name = 'expense_page'),
    path('add-expense/', views.add_expense, name = 'add_expense'),
    path('delete-expense/<int:id>/', views.delete_expense, name = 'delete_expense'),
    path('edit-expense/<int:id>/',views.edit_expense,name="edit_expense"),
    path('expense-sort/',views.expense_page_sort,name="expense_page_sort"),
    # path('expense-summary-data', api.expense_summary,name="expense_summary_data"),
    path('expense-summary/',views.expense_summary,name="expense_summary"),
    path('expense_summary_category/', views.expense_summary_category, name = "expense_summary_category"),
]
