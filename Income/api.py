from django.contrib.auth.decorators import login_required
# import login_required for mandatory login
import datetime
# import datetime module
from django.http import JsonResponse
# import JsonResponse for api data which is parsed in Json format
from datetime import timedelta
# from datetime import timedelta
from .models import Source,Income
# from Income models import Source and Income class

# function for api call for displaying income data in the form of charts
# login required
@login_required(login_url='login')
def income_summary(request):
    today_date = datetime.date.today()
    filter_by = request.GET.get('filter', None)
    if filter_by != None:
        # to get the incomes per category per week
        if filter_by.lower() == 'week':
            date_search =  today_date - timedelta(days=7) 
            incomes = Income.objects.filter(user=request.user,date__gte=date_search)
            title = 'Incomes per source in this week'
        
        # to get the incomes per category for the month
        elif filter_by.lower() == 'month':
            incomes = Income.objects.filter(user=request.user,date__year=today_date.year,date__month=today_date.month)
            title = 'Incomes per source in this month'
        
        # to get the incomes per category for the year
        elif filter_by.lower() == 'year':
            incomes = Income.objects.filter(user=request.user,date__year=today_date.year)
            title = 'Incomes per source in this year'
        
        # to get the incomes per category for today
        elif filter_by.lower() == 'today':
            incomes = Income.objects.filter(user=request.user,date__exact=today_date)
            title = 'Incomes per source earned today'
        
        # else show data for six months
        else:
            six_months_ago = today_date - datetime.timedelta(days = 30*6)
            incomes = Income.objects.filter(user = request.user,date__gte=six_months_ago)
            title = 'Incomes per source in last six months'
    
    else:
        six_months_ago = today_date - datetime.timedelta(days = 30*6)
        incomes = Income.objects.filter(user = request.user,date__gte=six_months_ago)
        title = 'Incomes per source in last six months'
    
    final_rep = {}


    # get source
    def get_source(income):
        return income.source.source
    source_list = list(set(map(get_source,incomes)))
    
    # get income source amount
    def get_income_source_amount(source):
        amount = 0
        source = Source.objects.get(user = request.user,source=source)
        filtered_by_source = incomes.filter(source=source.id)
        for i in filtered_by_source:
            amount += i.amount
        return amount
    
    # show all the incomes in that category
    for x in incomes:
        for y in source_list :
            final_rep[y] = get_income_source_amount(y)
    
    return JsonResponse({
        'income_source_data':final_rep,
        'label_title':title
    },safe=False)
