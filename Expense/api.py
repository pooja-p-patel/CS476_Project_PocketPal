from django.contrib.auth.decorators import login_required
# import login_required for mandatory login
import datetime
# import datetime module
from datetime import timedelta
# from datetime import timedelta
from django.http import JsonResponse
# import JsonResponse for api data which is parsed in Json format
from .models import Expense, Category
# From Expense app import Expense and Category models
import json
# imported json
from django.db.models import Q
# import Q object to merge two querysets such as using & operator


# function for api call for displaying expense data in the form of charts
# login required
@login_required(login_url='login')
def expense_summary(request):
    today_date = datetime.date.today()
    # to get the data which are already populated excluding the null values
    filter_by = request.GET.get('filter', None)
    if filter_by != None:
        # to get the expenses per category per week
        if filter_by.lower() == 'week':
            date_search =  today_date - timedelta(days=7) 
            expenses = Expense.objects.filter(user=request.user,date__gte=date_search)
            title = 'Expenses per category in this week'

        # to get the expenses per category for the month
        elif filter_by.lower() == 'month':
            expenses = Expense.objects.filter(user=request.user,date__year=today_date.year,date__month=today_date.month)
            title = 'Expenses per category in this month'


        # to get the expenses per category for the year
        elif filter_by.lower() == 'year':
            expenses = Expense.objects.filter(user=request.user,date__year=today_date.year)
            title = 'Expenses per category in this year'


        # to get the expenses per category for today
        elif filter_by.lower() == 'today':
            expenses = Expense.objects.filter(user=request.user,date__exact=today_date)
            title = 'Expenses per category spent today'

        # else show data for six months
        else:
            six_months_ago = today_date - datetime.timedelta(days = 30*6)
            expenses = Expense.objects.filter(user = request.user,date__gte=six_months_ago)
            title = 'Expenses per category in last six months'

    # else show expense data for six months
    else:
        six_months_ago = today_date - datetime.timedelta(days = 30*6)
        expenses = Expense.objects.filter(user = request.user,date__gte=six_months_ago)
        title = 'Expenses per category in last six months'

    final_rep = {}

    # get category 
    def get_category(expense):
        return expense.category.name
    category_list = list(set(map(get_category,expenses)))

    # get expenses for that category
    def get_expense_category_amount(category):
        amount = 0
        category = Category.objects.get(name=category)
        filtered_by_category = expenses.filter(category=category.id)
        for i in filtered_by_category:
            amount += i.amount
        return amount

    # show all the expenses in that category
    for x in expenses:
        for y in category_list :
            final_rep[y] = get_expense_category_amount(y)
            
    return JsonResponse({
        'expense_category_data':final_rep,
        'label_title':title
    },safe=False)

