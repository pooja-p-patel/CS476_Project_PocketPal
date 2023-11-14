from django.contrib.auth.models import User
# import User model
import re
# import re for regular expressions
from django.views import View
# import views
from django.shortcuts import render,redirect
# import render function and redirect function
from django.contrib import messages, auth
# The line `from django.contrib import messages, auth` is importing the `messages` and `auth` modules
# from the `django.contrib` package.


# The `RegistrationView` class handles the registration process for a user, including validating input
# fields and creating a new user account.
class RegistrationView(View):

    def get(self, request):
        return render(request, 'user/register_part.html')
    
    def post(self, request):
        username = request.POST.get('username','')
        email = request.POST.get('email','')
        first_name = request.POST.get('first_name','')
        last_name = request.POST.get('last_name','')
        password = request.POST.get('password','')
        password2 = request.POST.get('password2','')

        context = {
            "username":username,
            "email":email,
            "last_name":last_name,
            "first_name":first_name,
        }

        list_context = list(context.values())
        if '' in list_context:
            messages.error(request,"All Fields are required")
            return render(request,'user/register_part.html',context=context)

        # The code block you provided is handling the registration process for a user. It checks if
        # the provided username and email do not already exist in the database. If they don't exist,
        # it checks if the provided passwords match and meet certain criteria (minimum length of 8
        # characters and containing a combination of uppercase, lowercase characters, and numbers). If
        # the passwords meet the criteria, it creates a new user account with the provided username,
        # email, first name, and last name. The user's password is set and saved securely. Finally, a
        # success message is displayed and the user is redirected to the login page.
        if not User.objects.filter(username=username).exists():
            if  not User.objects.filter(email=email).exists():
                if password != password2:
                    messages.error(request,"Passwords don't match")
                    return render(request,'user/register_part.html',context=context)
                if len(password) < 8:
                    messages.error(request,'Password is too short, minimum length is 8 characters')
                    return render(request,'user/register_part.html',context=context)
                if len(password) >= 8:
                    if not re.search("[a-z]", password):
                        messages.error(request,"Password must contain combination of uppercase, lowercase characters and numbers")
                        return render(request,'user/register_part.html',context=context)
                    if not re.search("[A-Z]", password):
                        messages.error(request,"Password must contain combination of uppercase, lowercase characters and numbers")
                        return render(request,'user/register_part.html',context=context)
                    if not re.search("[0-9]", password):
                        messages.error(request,"Password must contain combination of uppercase, lowercase characters and numbers")
                        return render(request,'user/register_part.html',context=context)
                user = User.objects.create_user(username=username,email=email,first_name=first_name,last_name=last_name)
                user.set_password(password)
                user.save()
                messages.success(request,'Student Account Created Succesfully.')
                return redirect('login')
            else:
                # The code `messages.error(request,'Email Already exists')` adds an error message to
                # the request object. This message will be displayed to the user when the page is
                # rendered.
                messages.error(request,'Email Already exists')
                return render(request,'user/register_part.html',context=context)
        else:
            messages.error(request,'Username Already exists')
            return render(request,'user/register_part.html',context=context)
        


# The above class is a login view in Python that handles the login functionality, including validation
# and authentication.
class LoginView(View):

    def get(self,request):
        return render(request,'user/login_part.html')

    def post(self,request):
        username = request.POST.get('username','')
        password = request.POST.get('password','')

        context = {
            "username":username,
        }

       # The code block is checking if the username and password fields are empty. If either of them
       # is empty, it adds an error message to the request object using the `messages.error()`
       # function and renders the login page again with the error message displayed. This ensures that
       # the user is prompted to enter both the username and password before attempting to log in.
        if username == '':
            messages.error(request,"Please Enter username")
            return render(request,'user/login_part.html',context=context)

        if password == '':
            messages.error(request,"Please Enter Password")
            return render(request,'user/login_part.html',context=context)

        # The code block is handling the login functionality.
        if username and password:
            user = auth.authenticate(username=username,password=password)

            if user and user.is_staff == False:
                auth.login(request,user)
                messages.success(request,"Welcome, "+ user.username + ". You are now logged in.")
                return redirect('dashboard')
            
            elif user and user.is_staff == True:
                messages.error(request, "Welcome Admin! Please login from Admin Sign-in page!")
                return redirect('index')

            else:
                messages.error(request,'Invalid credentials')
                return render(request,'user/login_part.html',context=context)
        else:
            messages.error(request,'Something went wrong.')
            return render(request,'user/login_part.html',context=context)


    
# The above class is a view for handling the login functionality for an admin user.
class AdminLoginView(View):

    def get(self,request):
        return render(request,'user/admin_login_part.html')
    
    def post(self,request):
        username = request.POST.get('username','')
        password = request.POST.get('password','')

        context = {
            "username":username,
        }

        # The code block is checking if the username and password fields are empty. If either of them
        # is empty, it adds an error message to the request object using the `messages.error()`
        # function and renders the login page again with the error message displayed. This ensures
        # that the user is prompted to enter both the username and password before attempting to log
        # in.
        if username == '':
            messages.error(request,"Please Enter username")
            return render(request,'user/login_part.html',context=context)

        if password == '':
            messages.error(request,"Please Enter Password")
            return render(request,'user/login_part.html',context=context)

        # The code block is handling the login functionality.
        if username and password:
            user = auth.authenticate(username=username,password=password)

            if user and user.is_staff == True:
                auth.login(request,user)
                messages.success(request,"Welcome, "+ user.username + ". You are now logged in.")
                return redirect('advisor_dashboard')
            
            elif user and user.is_staff == False:
                messages.error(request,"Welcome Student! Please login from Student Sign-in page!")
                return redirect('index')
            
            else:
                messages.error(request,'Invalid credentials')
                return render(request,'user/login_part.html',context=context)
        else:
            messages.error(request,'Something went wrong.')
            return render(request,'user/login_part.html',context=context)


# The `LogoutView` class is a view in a Python web application that handles the logout functionality
# by logging out the user, displaying a success message, and redirecting to the index page.
class LogoutView(View):
	def post(self,request):
		auth.logout(request)
		messages.success(request,'Logged Out')
		return redirect('index')
