# from django.contrib.auth import get_user_model
# from rest_framework.views import APIView
# from .serializers import UserDataSerializers
# from rest_framework.response import Response
# from rest_framework import permissions, status

from django.contrib.auth.models import User
import re
from django.views import View
from django.shortcuts import render,redirect
from django.contrib import messages, auth
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode


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
                messages.error(request,'Email Already exists')
                return render(request,'user/register_part.html',context=context)
        else:
            messages.error(request,'Username Already exists')
            return render(request,'user/register_part.html',context=context)
        


class LoginView(View):

    def get(self,request):
        return render(request,'user/login_part.html')

    def post(self,request):
        username = request.POST.get('username','')
        password = request.POST.get('password','')

        context = {
            "username":username,
        }

        if username == '':
            messages.error(request,"Please Enter username")
            return render(request,'user/login_part.html',context=context)

        if password == '':
            messages.error(request,"Please Enter Password")
            return render(request,'user/login_part.html',context=context)

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


    
class AdminLoginView(View):

    def get(self,request):
        return render(request,'user/admin_login_part.html')
    
    def post(self,request):
        username = request.POST.get('username','')
        password = request.POST.get('password','')

        context = {
            "username":username,
        }

        if username == '':
            messages.error(request,"Please Enter username")
            return render(request,'user/login_part.html',context=context)

        if password == '':
            messages.error(request,"Please Enter Password")
            return render(request,'user/login_part.html',context=context)

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


class LogoutView(View):
	def post(self,request):
		auth.logout(request)
		messages.success(request,'Logged Out')
		return redirect('index')



# User = get_user_model()

# class RegistrationView(APIView):
#     permission_classes = (permissions.AllowAny, )

#     def post(self, request):
#         try:
#             data = request.data
#             firstName = data['firstName']
#             lastName = data['lastName']
#             email = data['email']
#             email = email.lower()
#             password = data['password']
#             confirmPassword = data['confirmPassword']
#             is_student = data['is_student']

#             if is_student == 'True':
#                 is_student = True
#             else:
#                 is_student = False

#             if password == confirmPassword:
#                 if len(password) >= 8:
#                     if not User.objects.filter(email=email).exists():
#                         if not is_student:
#                             User.objects.create_user(firstName=firstName, lastName=lastName, email=email,password=password)

#                             return Response(
#                                 {'success': 'Advisor account created successfully'},
#                                 status = status.HTTP_201_CREATED
#                             )
#                         else:
#                             User.objects.create_student(firstName=firstName, lastName=lastName, email=email,password=password)

#                             return Response(
#                                 {'success': 'Student account created successfully'},
#                                 status = status.HTTP_201_CREATED
#                             )    
#                     else:
#                         return Response(
#                             {'error': 'User with this email already exist!' },
#                             status = status.HTTP_400_BAD_REQUEST
#                         )
                    
#                 else:
#                     return Response(
#                         {'error': 'Passwords must be of eight characters or more' },
#                         status = status.HTTP_400_BAD_REQUEST
#                     )

#             else:
#                 return Response(
#                     {'error': 'Passwords do not match, please re-enter password' },
#                     status = status.HTTP_400_BAD_REQUEST
#                 )

#         except:
#             return Response(
#                 {'error': 'Something went wrong while registering the user'},
#                 status = status.HTTP_500_INTERNAL_SERVER_ERROR
#             )
        



# class GetUserView(APIView):
#     def get(self, request, format = None):
#         try:
#             user = request.user
#             user = UserDataSerializers(user)

#             return Response(
#                 {'user': user.data},
#                 status = status.HTTP_200_OK
#             )

#         except:
#             return Response(
#                 {'error': 'Something went wrong while getting user details'},
#                 status = status.HTTP_500_INTERNAL_SERVER_ERROR
#             )
