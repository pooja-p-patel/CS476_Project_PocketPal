from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from advisor.models import Comment
from .models import Flag, Student_Flag


# Create your views here.

@login_required(login_url='login')
def ask_advice(request):
    
    if request.method == 'GET':
        if Flag.objects.filter(user = request.user).exists():
            flag = Flag.objects.filter(user=request.user)

            context = {
                'flag' : flag,
            }

            return render(request,'advisor/ask_advice.html', context)
            
        else:
            return render(request,'advisor/ask_advice.html') 
    
    if request.method == 'POST':
        flag = Flag.objects.create(user = request.user)
        flag.my_flag = True
        flag.save()
        flag = Flag.objects.filter(user=request.user)
        context = {
            'flag' : flag,
        }
        messages.success(request,'You have submitted a request for an advice Successfully')
        return render(request,'advisor/ask_advice.html', context)
    

def check_advice(request):

    user = request.user
    if Student_Flag.objects.filter(user = user).exists():
        messages.success(request, 'Voila! You received the advice you have requested for!')

    if Comment.objects.filter(user = user).exists():
        comments = Comment.objects.filter(user = user)
        return render(request, 'advisor/check_advice.html', {'comments':comments})
    
    else:
        comments = 0
        return render(request, 'advisor/check_advice.html',{'comments':comments})

