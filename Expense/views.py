from django.shortcuts import render,redirect
# import render and redirect functions
from django.contrib.auth.decorators import login_required
# import login_required for mandatory login
from .models import Expense, Category
# from Expense.models import Expense and Category class
from Income.models import Source
# from Source.models import Source class
from django.contrib import messages
# import messages for showing message notifications
from django.utils.timezone import localtime
# from django.utils.timezone import localtime
from django.core.paginator import Paginator
# import paginator object for pagination 
import datetime
# import datetime module
from datetime import datetime as datetime_custom
# import datetime and use an alias datetime_custome 
from django.db.models import Q
# import Q object to merge two querysets such as using & operator


# function to show expense views
# login required
@login_required(login_url='login')
def expense_page(request):

    filter_context = {}
    base_url = f''
    date_from_html = ''
    date_to_html = ''

    expenses =  Expense.objects.filter(
        user = request.user
    ).order_by('-date')

    try:
        # code for pagination
        #  code for if the date for date from is empty while request method is get
        if 'date_from' in request.GET and request.GET['date_from'] != '':
            date_from = datetime_custom.strptime(request.GET['date_from'],'%Y-%m-%d')
            filter_context['date_from'] = request.GET['date_from']
            date_from_html = request.GET['date_from']

        #  code for if the date for date to is empty while request method is get
            if 'date_to' in request.GET and request.GET['date_to'] != '':

                date_to = datetime_custom.strptime(request.GET['date_to'],'%Y-%m-%d')
                filter_context['date_to'] = request.GET['date_to']
                date_to_html = request.GET['date_to']
                expenses = expenses.filter(
                    Q(date__gte = date_from )
                    &
                    Q(date__lte = date_to)
                ).order_by('-date')

            # else get expenses from the dates greater than from the comment dated for
            else:
                expenses = expenses.filter(
                    date__gte = date_from
                ).order_by('-date')

        elif 'date_to' in request.GET and request.GET['date_to'] != '':

            # else get expenses from dates lower than from the comment dated (date to)
            date_to_html = request.GET['date_to']
            date_to = datetime_custom.strptime(request.GET['date_to'],'%Y-%m-%d')
            filter_context['date_from'] = request.GET['date_to']
            expenses = expenses.filter(
                date__lte = date_to
            ).order_by('-date')
    
    except:
        # sends an error message that something is wrong
        messages.error(request,'Something went wrong')
        return redirect('expense_page')
    
    # store the data value into the variables
    base_url = f'?date_from={date_from_html}&date_to={date_to_html}&'
    paginator = Paginator(expenses,5)
    page_number = request.GET.get('page')
    page_expenses = Paginator.get_page(paginator,page_number)

    # render the templates by sending the variable values to the template for front-end view logic
    # sent values for pagination and expenses
    return render(request,'expense/expense.html',{
        'page_expenses':page_expenses,
        'expenses':expenses,
        'filter_context':filter_context,
        'base_url':base_url
    })


# login required
@login_required(login_url='login')
def add_expense(request):

    categories = Category.objects.all()
    sources = Source.objects.all()

    context = {
        'categories' : categories,
        'sources' : sources, 
    }


    # render add_expense page when it is a get request
    if request.method == 'GET':
        return render(request,'expense/add_expense.html',context)

    # store the form input values for post request
    if request.method == 'POST':
        amount = request.POST.get('amount','')
        description = request.POST.get('description','')
        category = request.POST.get('category','')
        source = request.POST.get('source', '')
        date = request.POST.get('expense_date','')

        # display an error is the field is empty
        if amount== '':
            messages.error(request,'Amount cannot be empty')
            return render(request,'expense/add_expense.html', context)
        
        # amount is stored in float
        amount = float(amount)
        if amount <= 0:
            messages.error(request,'Amount should be greater than zero')
            return render(request,'expense/add_expense.html', context)

        if description == '':
            messages.error(request,'Description cannot be empty')
            return render(request,'expense/add_expense.html', context)

        if category == '':
            messages.error(request,'Category cannot be empty')
            return render(request,'expense/add_expense.html', context)
        
        if source == '':
            messages.error(request,'Expense Account cannot be empty')
            return render(request,'expense/add_expense.html', context)

        # add localtime if date is not added
        if date == '':
            date = localtime()

        # store the created at time for the expense instance
        created_at = datetime.datetime.now().strftime ("%Y-%m-%d %H:%M:%S")

        # get the category names from the category objects
        category_obj = Category.objects.get(name =category)
        # get the source name from the source/account objects
        source_obj = Source.objects.get(source = source)
        # create expense object and save it
        Expense.objects.create(
            user=request.user,
            amount=amount,
            date=date,
            description=description,
            category=category_obj,
            source = source_obj,
            created_at = created_at,
        ).save()

        # show success message for expense saved
        messages.success(request,'Expense Saved Successfully')
        # redirect to the expense page view
        return redirect('expense_page')
    


# function to edit expense
# login required
@login_required(login_url='login')
def edit_expense(request,id):
    
    if Expense.objects.filter(id=id,user=request.user).exists():
        expense = Expense.objects.get(id=id,user=request.user)
    
    else:
        messages.error(request,'Something went Wrong. Please Try Again')
        return redirect('expense')
    
    # added some validation
    if expense.user != request.user:
        messages.error(request,'Something Went Wrong')
        return redirect('expense')
    
    # get category and source objects value
    categories = Category.objects.all().exclude(id = expense.category.id)
    sources = Source.objects.all().exclude(id = expense.source.id)

    context = {
        'expense': expense,
        'values': expense,
        'categories': categories,
        'sources': sources,  
    }
    
    # render edit expense template
    if request.method == 'GET':
        return render(request,'expense/edit_expense.html',context)

    # store the form input values on post request
    if request.method == 'POST':
        amount = request.POST.get('amount','')
        description = request.POST.get('description','')
        category = request.POST.get('category','')
        source = request.POST.get('source','')
        date = request.POST.get('expense_date','')
        
        # display an error message if the input value is empty
        if amount== '':
            messages.error(request,'Amount cannot be empty')
            return render(request,'expense/edit_expense.html',context)
        
        amount = float(amount)
        if amount <= 0:
            messages.error(request,'Amount should be greater than zero')
            return render(request,'expense/edit_expense.html',context)
        
        if description == '':
            messages.error(request,'Description cannot be empty')
            return render(request,'expense/edit_expense.html',context)
        
        if category == '':
            messages.error(request,'Expense Category cannot be empty')
            return render(request,'expense/edit_expense.html',context)
        
        if source == '':
            messages.error(request,'Expense Account cannot be empty')
            return render(request,'expense/edit_expense.html',context)
        
        # store the current localtime if date field is empty
        if date == '':
            date = localtime()
        
        # store the expense creation date and time
        created_at = datetime.datetime.now().strftime ("%Y-%m-%d %H:%M:%S")

        # get the category object for selected category name 
        category_obj = Category.objects.get(name =category)
        # get the source object for selected source/account name
        source_obj = Source.objects.get(source=source)

        # store the input values to the expense object and save
        expense.amount = amount
        expense.date = date
        expense.category = category_obj
        expense.source = source_obj
        expense.description = description
        expense.created_at = created_at
        expense.save() 
        

        # return redirect to expense page
        messages.success(request,'Expense Updated Successfully')
        return redirect('expense_page')



# function to delete expense
# login required
@login_required(login_url='login')
def delete_expense(request,id):
    
    # get the expense object id for the expense object wanting to delete
    if Expense.objects.filter(id=id,user=request.user).exists():
        expense = Expense.objects.get(id=id,user=request.user)
        
        # if user is not the expense.user then display an error message
        if expense.user != request.user:
            messages.error(request,'Something Went Wrong')
            return redirect('expense_page')
        
        # delete the expense
        else:
            expense.delete()
            messages.success(request,'Expense Deleted Successfully')
            return redirect('expense_page')
        
    # return to expense page view 
    else:
        messages.error(request,'Something went Wrong. Please Try Again')
        return redirect('expense_page')



# function to display expense summary categorizing the source/account
# login required
@login_required(login_url='login')
def expense_summary(request):

    # collect all the object instances
    expenses = Expense.objects.filter(user = request.user)
    sources = Source.objects.filter(user = request.user)
    category = Category.objects.all()

    context = {
        'expenses' : expenses,
        'sources' : sources,
        'category' : category,
    }

    # render the expense_summary page
    if request.method == 'GET':
        return render(request, 'expense/expense_summary.html', context)
    
    # if method is post
    if request.method == 'POST':

        # get the source id for selected source
        id = request.POST.get('source')
        source_all = Source.objects.get(id = id)

        # show all the expenses for that particular source
        if Expense.objects.filter(source = source_all, user = request.user).exists():
            expenses = Expense.objects.filter(source = source_all)

            sources = Source.objects.filter(user = request.user)

            context = {
                'expenses' : expenses,
                'sources' : sources,
            }

            # render the expense_summary page view after successful message
            messages.success(request, "Filtered table for " + source_all.source + " is displayed: ")
            return render(request, 'expense/expense_summary.html', context)
        
        else:
            # get all the source values created by the user
            sources = Source.objects.filter(user = request.user)
            
            context = {
                'sources' : sources,
            }

            # render template and display message of no expenses found
            messages.success(request, "No expenses found for this account/source")
            return render(request, 'expense/expense_summary.html', context)



# function to display expense summary categorizing the category
# login required
@login_required(login_url='login')
def expense_summary_category(request):

    # get all the expenses by user and show all categories
    expenses = Expense.objects.filter(user = request.user)
    categories = Category.objects.all()

    context = {
        'expenses' : expenses,
        'categories' : categories,
    }

    # render expense_summary page
    if request.method == 'GET':
        return render(request, 'expense/expense_summary_category.html', context)
    
    # if method is post
    if request.method == 'POST':

        # get id of the category selected
        id = request.POST.get('category')
        category_all = Category.objects.get(id = id)

        # get the expenes of the objects having the selected category
        if Expense.objects.filter(category = category_all, user = request.user).exists():
            expenses = Expense.objects.filter(category = category_all)

            categories = Category.objects.all()

            context = {
                'expenses' : expenses,
                'categories' : categories,
            }

            # update the table
            messages.success(request, "Filtered table for " + category_all.name + " is displayed: ")
            return render(request, 'expense/expense_summary_category.html', context)
        
        else:
            categories = Category.objects.all()

            context = {
                'categories' : categories,
            }

            #  render expense summary for category template 
            messages.success(request, "No expenses found for this category ")
            return render(request, 'expense/expense_summary_category.html', context)
