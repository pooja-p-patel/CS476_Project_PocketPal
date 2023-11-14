from django.shortcuts import render
# import render function 
from django.contrib.auth.decorators import login_required
# import login function which is required mandatory for users to log-in
from django.contrib import messages
# import messages to notify user
from advisor.models import Comment
# import comment class from advisor model
from .models import Flag, Student_Flag
# import Flag and Student_Flag class from advice model


# function to ask advice
# login required
@login_required(login_url='login')
def ask_advice(request):
    
    # if the request method is get 
    if request.method == 'GET':
        if Flag.objects.filter(user = request.user).exists():
            flag = Flag.objects.filter(user=request.user)

            context = {
                'flag' : flag,
            }

            return render(request,'advisor/ask_advice.html', context)
           
        # if Flag class object doesn't have requested user flag then render the ask_advice template    
        else:
            return render(request,'advisor/ask_advice.html') 
    
    # if the request method is post
    if request.method == 'POST':
        # create a flag object with the user field as request.user
        flag = Flag.objects.create(user = request.user)
        # change the boolean flag to true
        flag.my_flag = True
        # save the object instance
        flag.save()
        flag = Flag.objects.filter(user=request.user)
        context = {
            'flag' : flag,
        }
        # success message and render the ask_advice template
        messages.success(request,'You have submitted a request for an advice Successfully')
        return render(request,'advisor/ask_advice.html', context)


# function for check_advice
# login required
@login_required(login_url='login')
def check_advice(request):

    # if flag of user [Student_Flag] object instace is true then send a message to the student user
    user = request.user
    if Student_Flag.objects.filter(user = user).exists():
        messages.success(request, 'Voila! You received the advice you have requested for!')

    # To get and show what comments are commented by the admin after student user requested advice
    if Comment.objects.filter(user = user).exists():
        comments = Comment.objects.filter(user = user)
        return render(request, 'advisor/check_advice.html', {'comments':comments})
    
    # if no comments then render the check_advice template
    else:
        comments = 0
        return render(request, 'advisor/check_advice.html',{'comments':comments})

