from django.shortcuts import render, redirect
# import render and redirect functions
from django.urls import reverse
# import reverse function for reverse render request
from advise.models import Flag, Student_Flag
# import Flag and Student_Flag class from advice model
from django.contrib.auth.models import User
# import User model
from django.contrib.auth.decorators import login_required
# import login_required for mandatory login
from django.core.paginator import Paginator
# import paginator object for pagination 
from django.contrib import messages
# import messages for showing message notifications
from django.db.models import Q
# import Q object to merge two querysets such as using & operator
from datetime import datetime
# import datetime object from datetime
import datetime
# import datetime module
from datetime import datetime as datetime_custom
# import datetime and use an alias datetime_custome 
from advisor.models import Comment, Observer
# import Comment and Observer class from advisor model


# function for displaying advisor_dashboard
# login required
@login_required(login_url='login')
def advisor_dashboard(request):
    flagged_users = Flag.objects.all()
    context = {
        'flagged_users': flagged_users,
    }
    return render(request, 'advisor_dashboard.html', context)



# login required
# function to diplay all the comments commented by the admin
@login_required(login_url='login')
def comment(request):

    filter_context = {}
    base_url = f''
    date_from_html = ''
    date_to_html = ''

    comments =  Comment.objects.all()

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
                comments = comments.filter(
                    Q(date__gte = date_from )
                    &
                    Q(date__lte = date_to)
                ).order_by('-date')

            # else get comments from the dates greater than from the comment dated for
            else:
                comments = comments.filter(
                    date__gte = date_from
                ).order_by('-date')

        elif 'date_to' in request.GET and request.GET['date_to'] != '':

            # else get comments from dates lower than from the comment dated (date to)
            date_to_html = request.GET['date_to']
            date_to = datetime_custom.strptime(request.GET['date_to'],'%Y-%m-%d')
            filter_context['date_from'] = request.GET['date_to']
            comments = comments.filter(
                date__lte = date_to
            ).order_by('-date')
    
    except:
        # sends an error message that something is wrong
        messages.error(request,'Something went wrong')
        return redirect('comment')
    
    # store the data value into the variables
    base_url = f'?date_from={date_from_html}&date_to={date_to_html}&'
    paginator = Paginator(comments,5)
    page_number = request.GET.get('page')
    page_comments = Paginator.get_page(paginator,page_number)
    flagged_users = Flag.objects.all()

    # render the templates by sending the variable values to the template for front-end view logic
    # sent values for pagination and flagged_users
    return render(request,'advisor/comment.html',{
        'page_comments':page_comments,
        'comments':comments,
        'filter_context':filter_context,
        'base_url':base_url,
        'flagged_users': flagged_users,
    })


# function to add comment
# login required
@login_required(login_url='login')
def add_comment(request,pk):

    flagged_users = Flag.objects.all()
    user = User.objects.get(id = pk)

    context = {
        'flagged_users' : flagged_users,
        'user' : user,
    }

    # render the add_commment template on get request
    if request.method == 'GET':
        return render(request,'advisor/add_comment.html',context)

    # store the form values if post request
    if request.method == 'POST':
        name = request.POST.get('name','')
        body = request.POST.get('body','')
        requested_user = request.POST.get('requested_user','')

    # if the fields are emply throw and error
        if name== '':
            messages.error(request,'Comment title cannot be empty')
            return render(request,'advisor/add_comment.html', context)
        
        if body== '':
            messages.error(request,'Comment cannot be empty')
            return render(request,'advisor/add_comment.html', context)

        if requested_user == '':
            messages.error(request,'user cannot be empty')
            return render(request,'advisor/add_comment.html', context)

    # store the time and date for the comment created
        date = datetime.datetime.now().strftime ("%Y-%m-%d %H:%M:%S")

        user = User.objects.get(id = pk)

    # create a comment object for the student user using Comment class
    # A Comment object instace for the student user has been created and saved in the database
        Comment.objects.create(
            name = name,
            student_name = requested_user,
            created_on=date,
            body=body,
            user=user,
        ).save()

        # After the comment is created add the student user for whom the comment
        # is commented to the Observer database table

        # if the student user for which the comment is commented exist 
        # in the observer table then it grabs the user object of the 
        # student user inside the observer table
        if Observer.objects.filter(user = user).exists():
            user = User.objects.get(id = pk)

        # if the Student user does not exist in the observer table then
        # add the student user to the Observer table  
        else:
            Observer.objects.create(
                user = user,
            ).save()
            user = User.objects.get(id = pk)

        # Notify the student_flag object instance when the student user 
        # is added to the Observer list to true
        if Student_Flag.objects.filter(user = user).exists():
            pass
        else:
            student_flag = Student_Flag.objects.create(user = user)
            student_flag.my_advice = True
            student_flag.save()

        comments = Comment.objects.filter(user = user)
        context = {
            'user' : user,
            'comments' : comments,
            'values' : comments,
        }

        # render the view dashboard page to show student analytics
        messages.success(request,'Comment Saved Successfully')
        return render(request, 'view_dashboard.html', context)
    


# function to edit comment
# login required
@login_required(login_url='login')
def edit_comment(request,pk):
    
    # if the comment already exist get the comment 
    if Comment.objects.filter(id = pk).exists():
        comment = Comment.objects.get(id = pk)
    
    # else show error message that there is something wrong
    else:
        messages.error(request,'Something went Wrong. Please Try Again')
        return redirect(reverse('comment'))

    context = {
        'comment':comment,
        'values': comment,
    }
    
    # render the edit comment page on get request method
    if request.method == 'GET':
        return render(request,'advisor/edit_comment.html',context)

    # on post request store the values from the form once submitted
    if request.method == 'POST':
        name = request.POST.get('name','')
        body = request.POST.get('body','')
        requested_user = request.POST.get('requested_user','')
        
        # display an error if fields are empty
        if name== '':
            messages.error(request,'Comment title cannot be empty')
            return render(request,'advisor/add_comment.html', context)
        
        if body== '':
            messages.error(request,'Comment cannot be empty')
            return render(request,'advisor/add_comment.html', context)

        if requested_user == '':
            messages.error(request,'user cannot be empty')
            return render(request,'advisor/add_comment.html', context)

        # add the date and time of its creation
        date = datetime.datetime.now().strftime ("%Y-%m-%d %H:%M:%S")
        
        user_data = comment.user

        # save the edited comment object instance
        comment.name = name
        comment.student_name = requested_user
        comment.created_on = date
        comment.user = user_data
        comment.body = body
        comment.save() 

        # return redirect to comment template
        messages.success(request,'Comment Saved Successfully')
        return redirect(reverse('comment'))
    


# function to delete comment
# login required
@login_required(login_url='login')
def delete_comment(request,pk):
    
    # if comment exist then delete the comment
    if Comment.objects.filter(id=pk).exists():
        comment = Comment.objects.get(id=pk)
        
        comment.delete()
        messages.success(request,'Comment Deleted Successfully')
        return redirect('comment')
    else:
        messages.error(request,'Something went Wrong. Please Try Again')
        return redirect('comment')
