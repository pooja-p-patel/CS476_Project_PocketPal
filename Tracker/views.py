from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Expense.models import Expense
from django.contrib.auth.models import User
from advisor.models import Comment
from Income.models import Income
from advise.models import Student_Flag
from django.contrib import messages
from datetime import timedelta
from django.db.models import Sum
from django.http import HttpResponse
from django.utils.timezone import localtime
import datetime

@login_required(login_url='login')
def dashboard(request):
    today_date_time = localtime()
    today_date = datetime.date.today()
    week_date_time = today_date - timedelta(days=7) 
    # week_date_time = today_date - timedelta(days=30)
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
        # 'comments' : comments,
    })

