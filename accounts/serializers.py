from rest_framework.serializers import ModelSerializer 
from rest_framework import serializers 
from django.contrib.auth.models import User 
from django.contrib.auth.password_validation import validate_password 


class UserSerializer(ModelSerializer):
    class Meta:
        model = User 
        fields = ['id', 'username', 'email']
        
        
class RegisterSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)
    
    class Meta:
        model = User 
        fields = ['username', 'password', 'password2']
        
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Password do not match")
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('User with this username elready exists')
        return data 
    
    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
        return user     
         