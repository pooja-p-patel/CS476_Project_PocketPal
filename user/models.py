from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# class AccountManager(BaseUserManager):
#     def create_user(self, email, firstName, lastName, password = None):
#         if not email:
#             raise ValueError("User must have an Email-Address to create an Account")
        
#         email = self.normalize_email(email) 
#         email = email.lower()

#         user = self.model(
#             email = email,
#             firstName = firstName,
#             lastName = lastName
#         )

#         user.set_password(password)
#         user.save()

#         return user
    
#     def create_student(self, email, firstName, lastName, password = None):
#         user = self.create_user(email, firstName, lastName, password)
        
#         user.is_student = True
#         user.save()

#         return user
    
#     def create_superuser(self, email, firstName, lastName, password = None):
#         user = self.create_user(email, firstName, lastName, password)

#         user.is_superuser = True
#         user.is_staff = True

#         user.save()
#         return user

# class Account(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(max_length=255, unique=True)
#     firstName = models.CharField(max_length=255)
#     lastName = models.CharField(max_length=255)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)

#     is_student = models.BooleanField(default=True)

#     objects = AccountManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['firstName', 'lastName']

#     def __str__(self):
#         return self.email

