from django.shortcuts import render
# import render function
from django.contrib.auth.decorators import login_required
# import login_required for mandatory login
from Expense.models import Expense
# import expense class from Expense.models
from django.contrib.auth.models import User
# import User model
from Income.models import Income
# from Income.models import Income class
from advise.models import Student_Flag
# from advise.models import Student_Flag class
from django.contrib import messages
# import messages for showing message notifications
from datetime import timedelta
# from datetime import timedelta
from django.db.models import Sum
# import sum 
from django.utils.timezone import localtime
# `# import localtime` is importing the `localtime` function from the `django.utils.timezone` module.
# This function is used to get the current date and time in the local timezone.
import datetime
# The line `import datetime` is importing the `datetime` module from the Python standard library. This
# module provides classes for working with dates and times. In this code, the `datetime` module is
# used to perform various date and time calculations and operations.



# login required
@login_required(login_url='login')
def dashboard(request):
    """
    The `dashboard` function retrieves and displays various financial data for the current user,
    including expenses and incomes for today, as well as totals and counts for the current day, month,
    week, and year.
    
    :param request: The request object represents the HTTP request that is made to the server. It
    contains information such as the user making the request, the method used (GET or POST), and any
    data sent with the request
    :return: a rendered HTML template called 'dashboard2.html' with various data passed as context
    variables. The data includes expenses and incomes for today, the total amount spent today, the count
    of expenses made today, the total amount spent this month, the count of expenses made this month,
    the total amount spent this year, the count of expenses made this year, the total amount spent in
    the
    """
    today_date_time = localtime()
    today_date = datetime.date.today()
    week_date_time = today_date - timedelta(days=7) 
    start_today_data = today_date_time.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_today_data = today_date_time.replace(day=30 ,hour=23, minute=59, second=59, microsecond=999999)

    incomes_today_display = Income.objects.filter(user=request.user,created_at__range=(start_today_data,end_today_data)).order_by('-created_at')
    expenses_today_display = Expense.objects.filter(user=request.user,created_at__range=(start_today_data,end_today_data)).order_by('-created_at')

    expenses_year = Expense.objects.filter(user=request.user,date__year=today_date.year)
    expenses_month = expenses_year.filter(date__month=today_date.month)
    expenses_today = expenses_month.filter(date__exact=today_date)
    expenses_week = expenses_month.filter(date__gte=week_date_time)

    spent_year_count = expenses_year.count()
    spent_month_count = expenses_month.count()
    spent_today_count = expenses_today.count()
    spent_week_count = expenses_week.count()
    spent_month = expenses_month.aggregate(Sum('amount'))
    spend_today = expenses_today.aggregate(Sum('amount'))
    spent_week = expenses_week.aggregate(Sum('amount'))
    spent_year = expenses_year.aggregate(Sum('amount'))

    user = request.user
    if Student_Flag.objects.filter(user = user).exists():
        messages.success(request, 'Voila! You received the advice you have requested for!')

    return render(request,'dashboard2.html',{
        'expenses':expenses_today_display[:5],
        'incomes':incomes_today_display[:5],
        'spent_today':spend_today['amount__sum'],
        'spent_today_count':spent_today_count,
        'spent_month':spent_month['amount__sum'],
        'spent_month_count':spent_month_count,
        'spent_year':spent_year['amount__sum'],
        'spent_year_count':spent_year_count,
        'spent_week':spent_week['amount__sum'],
        'spent_week_count':spent_week_count,
    })



@login_required(login_url='login')
def view_dashboard(request,pk): 
    """
    The `view_dashboard` function retrieves financial data for a student user 
    and renders it in an admin dashboard template.
    
    :param request: The request object represents the HTTP request that was made by the user
    :param pk: The parameter "pk" is the primary key of a user. It is used to retrieve the user object
    from the database
    :return: a rendered HTML template called 'view_dashboard.html' with various data passed as context
    variables. The data includes expenses and incomes for today, the total amount spent today, the count
    of expenses made today, the total amount spent this month, the count of expenses made this month,
    the total amount spent this year, the count of expenses made this year, the total amount spent in
    the
    """
    today_date_time = localtime()
    today_date = datetime.date.today()
    week_date_time = today_date - timedelta(days=7) 
    start_today_data = today_date_time.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_today_data = today_date_time.replace(day=30, hour=23, minute=59, second=59, microsecond=999999)

    user = User.objects.get(id = pk)
    incomes_today_display = Income.objects.filter(user = user,created_at__range=(start_today_data,end_today_data)).order_by('-created_at')
    expenses_today_display = Expense.objects.filter(user = user,created_at__range=(start_today_data,end_today_data)).order_by('-created_at')

    expenses_year = Expense.objects.filter(user = user,date__year=today_date.year)
    expenses_month = expenses_year.filter(date__month=today_date.month)
    expenses_today = expenses_month.filter(date__exact=today_date)
    expenses_week = expenses_month.filter(date__gte=week_date_time)

    spent_year_count = expenses_year.count()
    spent_month_count = expenses_month.count()
    spent_today_count = expenses_today.count()
    spent_week_count = expenses_week.count()
    spent_month = expenses_month.aggregate(Sum('amount'))
    spend_today = expenses_today.aggregate(Sum('amount'))
    spent_week = expenses_week.aggregate(Sum('amount'))
    spent_year = expenses_year.aggregate(Sum('amount'))

    user = User.objects.get(id = pk)

    return render(request,'view_dashboard.html',{
        'expenses':expenses_today_display[:5],
        'incomes':incomes_today_display[:5],
        'spent_today':spend_today['amount__sum'],
        'spent_today_count':spent_today_count,
        'spent_month':spent_month['amount__sum'],
        'spent_month_count':spent_month_count,
        'spent_year':spent_year['amount__sum'],
        'spent_year_count':spent_year_count,
        'spent_week':spent_week['amount__sum'],
        'spent_week_count':spent_week_count,
        'user' : user,
    })

