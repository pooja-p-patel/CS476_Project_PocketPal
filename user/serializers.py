from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserDataSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('firstName','lastName','email','is_student', )