from django.shortcuts import render, redirect
from django.urls import reverse
from advise.models import Flag, Student_Flag
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from datetime import datetime
import datetime
from django.utils.timezone import localtime
from datetime import datetime as datetime_custom
from advisor.models import Comment, Observer
from django.db.models import Sum
import datetime
from datetime import timedelta


# Create your views here.

@login_required(login_url='login')
def advisor_dashboard(request):
    flagged_users = Flag.objects.all()
    context = {
        'flagged_users': flagged_users,
    }
    return render(request, 'advisor_dashboard.html', context)


@login_required(login_url='login')
def comment(request):

    filter_context = {}
    base_url = f''
    date_from_html = ''
    date_to_html = ''

    comments =  Comment.objects.all()

    try:

        if 'date_from' in request.GET and request.GET['date_from'] != '':
            date_from = datetime_custom.strptime(request.GET['date_from'],'%Y-%m-%d')
            filter_context['date_from'] = request.GET['date_from']
            date_from_html = request.GET['date_from']

            if 'date_to' in request.GET and request.GET['date_to'] != '':

                date_to = datetime_custom.strptime(request.GET['date_to'],'%Y-%m-%d')
                filter_context['date_to'] = request.GET['date_to']
                date_to_html = request.GET['date_to']
                comments = comments.filter(
                    Q(date__gte = date_from )
                    &
                    Q(date__lte = date_to)
                ).order_by('-date')

            else:
                comments = comments.filter(
                    date__gte = date_from
                ).order_by('-date')

        elif 'date_to' in request.GET and request.GET['date_to'] != '':

            date_to_html = request.GET['date_to']
            date_to = datetime_custom.strptime(request.GET['date_to'],'%Y-%m-%d')
            filter_context['date_from'] = request.GET['date_to']
            comments = comments.filter(
                date__lte = date_to
            ).order_by('-date')
    
    except:
        messages.error(request,'Something went wrong')
        return redirect('comment')
    
    base_url = f'?date_from={date_from_html}&date_to={date_to_html}&'
    paginator = Paginator(comments,5)
    page_number = request.GET.get('page')
    page_comments = Paginator.get_page(paginator,page_number)
    flagged_users = Flag.objects.all()

    return render(request,'advisor/comment.html',{
        'page_comments':page_comments,
        'comments':comments,
        'filter_context':filter_context,
        'base_url':base_url,
        'flagged_users': flagged_users,
    })

@login_required(login_url='login')
def add_comment(request,pk):

    flagged_users = Flag.objects.all()
    user = User.objects.get(id = pk)

    context = {
        'flagged_users' : flagged_users,
        'user' : user,
    }

    if request.method == 'GET':
        return render(request,'advisor/add_comment.html',context)

    if request.method == 'POST':
        name = request.POST.get('name','')
        body = request.POST.get('body','')
        requested_user = request.POST.get('requested_user','')
        # date = request.POST.get('comment_date','')

        if name== '':
            messages.error(request,'Comment title cannot be empty')
            return render(request,'advisor/add_comment.html', context)
        
        if body== '':
            messages.error(request,'Comment cannot be empty')
            return render(request,'advisor/add_comment.html', context)

        if requested_user == '':
            messages.error(request,'user cannot be empty')
            return render(request,'advisor/add_comment.html', context)

        date = datetime.datetime.now().strftime ("%Y-%m-%d %H:%M:%S")

        user = User.objects.get(id = pk)

        Comment.objects.create(
            name = name,
            student_name = requested_user,
            created_on=date,
            body=body,
            user=user,
        ).save()

        if Observer.objects.filter(user = user).exists():
            user = User.objects.get(id = pk)
        else:
            Observer.objects.create(
                user = user,
            ).save()
            user = User.objects.get(id = pk)

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

        messages.success(request,'Comment Saved Successfully')
        return render(request, 'view_dashboard.html', context)
    
@login_required(login_url='login')
def edit_comment(request,pk):
    
    comment_data = Comment.objects.get(id = pk)
    
    if Comment.objects.filter(id = pk).exists():
        comment = Comment.objects.get(id = pk)
    
    else:
        messages.error(request,'Something went Wrong. Please Try Again')
        # return redirect(reverse('view_dashboard', kwargs={'pk': user_data.id}), args={'comment_data' : comment_data })
        return redirect(reverse('comment'))

    # if expense.user != request.user:
    #     messages.error(request,'Something Went Wrong')
    #     return redirect('expense')
    
    # flagged_users = Flag.objects.filter(user = user)

    context = {
        'comment':comment,
        'values': comment,
        # 'user': user_data,
    }
    
    if request.method == 'GET':
        return render(request,'advisor/edit_comment.html',context)

    if request.method == 'POST':
        name = request.POST.get('name','')
        body = request.POST.get('body','')
        requested_user = request.POST.get('requested_user','')
        # date = request.POST.get('comment_date','')
        
        if name== '':
            messages.error(request,'Comment title cannot be empty')
            return render(request,'advisor/add_comment.html', context)
        
        if body== '':
            messages.error(request,'Comment cannot be empty')
            return render(request,'advisor/add_comment.html', context)

        if requested_user == '':
            messages.error(request,'user cannot be empty')
            return render(request,'advisor/add_comment.html', context)

        date = datetime.datetime.now().strftime ("%Y-%m-%d %H:%M:%S")
        
        user_data = comment.user

        comment.name = name
        comment.student_name = requested_user
        comment.created_on = date
        comment.user = user_data
        comment.body = body
        comment.save() 

        messages.success(request,'Comment Saved Successfully')
        # return redirect('view_dashboard')
        return redirect(reverse('comment'))
    

@login_required(login_url='login')
def delete_comment(request,pk):
    
    if Comment.objects.filter(id=pk).exists():
        comment = Comment.objects.get(id=pk)
        
        comment.delete()
        messages.success(request,'Comment Deleted Successfully')
        return redirect('comment')
    else:
        messages.error(request,'Something went Wrong. Please Try Again')
        return redirect('comment')
