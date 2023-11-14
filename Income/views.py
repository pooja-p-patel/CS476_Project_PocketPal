from django.shortcuts import render, redirect
# import render and redirect functions
from .models import Source,Income
# from Income.models import Source and Income class
from django.contrib.auth.decorators import login_required
# import login_required for mandatory login
from django.contrib import messages
# import messages for showing message notifications
from django.core.paginator import Paginator
# import paginator object for pagination 
from django.utils.timezone import localtime
# from django.utils.timezone import localtime
import datetime
# import datetime module
from datetime import datetime as datetime_custom
# import datetime and use an alias datetime_custome 
from django.db.models import Q
# import Q object to merge two querysets such as using & operator


# function for viewing all incomes
# login required
@login_required(login_url='login')
def income_page(request):

    filter_context = {}
    base_url = f''
    date_from_html = ''
    date_to_html = ''

    incomes =  Income.objects.filter(
        user=request.user
    ).order_by('-date')

    # add pagination to the page
    try:

        if 'date_from' in request.GET and request.GET['date_from'] != '':
            date_from = datetime_custom.strptime(request.GET['date_from'],'%Y-%m-%d')
            filter_context['date_from'] = request.GET['date_from']
            date_from_html = request.GET['date_from']

            if 'date_to' in request.GET and request.GET['date_to'] != '':

                date_to = datetime_custom.strptime(request.GET['date_to'],'%Y-%m-%d')
                filter_context['date_to'] = request.GET['date_to']
                date_to_html = request.GET['date_to']
                incomes = incomes.filter(
                    Q(date__gte = date_from )
                    &
                    Q(date__lte = date_to)
                ).order_by('-date')

            else:
                incomes = incomes.filter(
                    date__gte = date_from
                ).order_by('-date')

        elif 'date_to' in request.GET and request.GET['date_to'] != '':

            date_to_html = request.GET['date_to']
            date_to = datetime_custom.strptime(request.GET['date_to'],'%Y-%m-%d')
            filter_context['date_from'] = request.GET['date_to']
            incomes = incomes.filter(
                date__lte = date_to
            ).order_by('-date')
        
    except:
        messages.error(request,'Something went wrong')
        return redirect('income')
    
    base_url = f'?date_from={date_from_html}&date_to={date_to_html}&'
    paginator = Paginator(incomes,5)
    page_number = request.GET.get('page')
    page_incomes = Paginator.get_page(paginator,page_number)
    
    return render(request,'income/income.html',{
        'page_incomes':page_incomes,
        'incomes':incomes,
        'filter_context':filter_context,
        'base_url':base_url
    })



# function to add income
# login required
@login_required(login_url='login')
def add_income(request):

    if Source.objects.filter(user=request.user).exists():

        sources = Source.objects.filter(user=request.user)

        context = {
            'sources' : sources,
            'values':request.POST
    	}

        # render add income page if method is get
        if request.method == 'GET':
            return render(request,'income/add_income.html',context)
        
        # for method is post request
        if request.method == 'POST':
            amount = request.POST.get('amount','')
            description = request.POST.get('description','')
            source = request.POST.get('source','')
            date = request.POST.get('income_date','')
            

            # store input values and check empty values
            if amount == '':
                messages.error(request,'Amount cannot be empty')
                return render(request,'income/add_income.html',context)
            
            amount = float(amount)
            if amount<=0 :
                messages.error(request,'Amount should be greater than zero')
                return render(request,'income/add_income.html',context)
            
            if description == '':
                messages.error(request,'Description cannot be empty')
                return render(request,'income/add_income.html',context)
            
            if source == '':
                messages.error(request,'IncomeSource cannot be empty')
                return render(request,'income_app/add_income.html',context)
            
            if date == '':
                date = localtime()

            created_at = datetime.datetime.now().strftime ("%Y-%m-%d %H:%M:%S")
            
            source_obj = Source.objects.get(user=request.user,source =source)
            Income.objects.create(
                user=request.user,
                amount=amount,
                date=date,
                description=description,
                source=source_obj,
                created_at= created_at,
            ).save()

            # income object created and saved
            messages.success(request,'Income Saved Successfully')
            return redirect('income')
    else:
        messages.error(request,'Please add a income source first.')
        return redirect('add_income_source')



# function to add income source
# login required
@login_required(login_url='login')
def add_income_source(request):

    sources = Source.objects.filter(user=request.user)
    
    context = {
        'sources' : sources,
        'values':request.POST,
        'create':True
    }

    # if method is get render the income source import template
    if request.method == 'GET': 
        return render(request,'income/income_source_import.html',context)
    
    # for post request
    if request.method == 'POST':
        source = request.POST.get('source','')
        
        if source == '':
            messages.error(request,'Income Source cannot be empty')
            return render(request,'income/income_source_import.html',context)
        
        source = source.lower().capitalize()
        if Source.objects.filter(user=request.user,source = source).exists():
            messages.error(request,f'Income Source ({source}) already exists.')
            return render(request,'income/income_source_import.html',context)
        
        # store values and create the source object
        date = datetime.datetime.now().strftime ("%Y-%m-%d %H:%M:%S")
        Source.objects.create(user=request.user,source = source,created_at = date).save()
        
        # success message
        messages.success(request,'IncomeSource added')
        return render(request,'income/income_source_import.html',{
            'sources' : sources,
            'create':True
        })


# function to edit income source
# login required
@login_required(login_url='login')
def edit_income_source(request,id):

    if Source.objects.filter(user=request.user,pk=id).exists():
        source_obj = Source.objects.get(user=request.user,pk=id)
    else:
        messages.error(request,'Something Went Wrong')
        return redirect('add_income_source')
    
    if source_obj.user != request.user:
        messages.error(request,'Something Went Wrong')
        return redirect('add_income_source')

    context = {
        'value' : source_obj.source,
        'update':True,
        'id':source_obj.id
    }

    # get the source object instance created by the requested user and render below page
    if request.method == 'GET': 
        return render(request,'income/income_source_import.html',context)
    
    # if method is post
    if request.method == 'POST':
        source = request.POST.get('source','')
        
        context = {
            'value':source,
            'update':True,
            'id':source_obj.id
        }

    # check empty fields
        if source == '':
            messages.error(request,'Income Source cannot be empty')
            return render(request,'income/income_source_import.html',context)
        
        source = source.lower().capitalize()
        if Source.objects.filter(user=request.user,source = source).exists():
            messages.error(request,f'Income Source ({source}) already exists.')
            return render(request,'income/income_source_import.html',context)
        
        # create source object and save
        source_obj.source = source
        source_obj.save()
        
        messages.success(request,'Income Source Updated')
        return redirect('add_income_source')


# function to delete income source
# login required
@login_required(login_url='login')
def delete_income_source(request,id):

    if Source.objects.filter(pk=id,user=request.user).exists():
        income_source = Source.objects.get(pk=id,user=request.user)
        
        # after getting the source id and check the user
        if income_source.user != request.user:
            messages.error(request,'You cannot delete this income source.')
            return redirect('add_income_source')
        
        # If source.user is requested user then delete the source
        else:
            income_source.delete()
            messages.success(request,'Deleted income source')
            return redirect('add_income_source')
    
    messages.error(request,'Please try again')
    return redirect('add_income_source')



# function to edit income
# login required
@login_required(login_url='login')
def edit_income(request,id):
    
    # get the income object instance for requested user
    if Income.objects.filter(id=id,user=request.user).exists():
        income = Income.objects.get(id=id,user=request.user)
    
    else:
        messages.error(request,'Something went Wrong. Please Try Again')
        return redirect('income')
    
    if income.user != request.user:
        messages.error(request,'Something Went Wrong')
        return redirect('income')

    sources = Source.objects.filter(user=request.user).exclude(id=income.source.id)

    context = {
        'income':income,
        'values': income,
        'sources':sources
    }
    
    # render edit income template
    if request.method == 'GET':
        return render(request,'income/edit_income.html',context)

    # if method is post
    if request.method == 'POST':
        amount = request.POST.get('amount','')
        description = request.POST.get('description','')
        source = request.POST.get('source','')
        date = request.POST.get('income_date','')
        
        # store all input values and check empty fields
        if amount== '':
            messages.error(request,'Amount cannot be empty')
            return render(request,'income/edit_income.html',context)
        
        amount = float(amount)
        if amount <= 0:
            messages.error(request,'Amount should be greater than zero')
            return render(request,'income/edit_income.html',context)
        
        if description == '':
            messages.error(request,'Description cannot be empty')
            return render(request,'income/edit_income.html',context)
        
        if source == '':
            messages.error(request,'Income Source cannot be empty')
            return render(request,'income/edit_income.html',context)
        
        if date == '':
            date = localtime()

        # get the date instance of income creation
        created_at = datetime.datetime.now().strftime ("%Y-%m-%d %H:%M:%S")
        
        # store the income object and save
        income_obj = Source.objects.get(user=request.user,source=source)
        income.amount = amount
        income.date = date
        income.source = income_obj
        income.description = description
        income.created_at = created_at
        income.save()

        messages.success(request,'Income Updated Successfully')
        return redirect('income')


# function to delete income
# login required
@login_required(login_url='login')
def delete_income(request,id):

    if Income.objects.filter(id=id,user=request.user).exists():
        income = Income.objects.get(id=id,user=request.user)
        
        if income.user != request.user:
            messages.error(request,'Something Went Wrong')
            return redirect('income')
        
        # if the income id and user matches then delete the user
        else:
            income.delete()
            messages.success(request,'Income Deleted Successfully')
            return redirect('income')
    else:
        messages.error(request,'Something went Wrong. Please Try Again')
        return redirect('income')
