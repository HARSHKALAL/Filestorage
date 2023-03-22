from .models import *
from rest_framework import serializers
from django.contrib.auth import  authenticate

class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=255,write_only=True)
    date_of_birth = serializers.DateField(required=True)
    class Meta:
        model = Signup
        fields = ('first_name','last_name','email','username','date_of_birth','password','confirm_password')

    def create(self, validated_data):
        instance = super().create(validated_data)
        raw_password = validated_data.get('password')
        instance.set_password(raw_password)
        instance.save()
        return instance

    def validate(self, attrs):
        password = attrs.get('password')
        confirmation_password = attrs.get('confirm_password')
        if not password == confirmation_password:
            raise serializers.ValidationError("PASSWORD DOESNOT MATCH")
        attrs.pop('confirm_password')
        return attrs

class ProjectSerializer(serializers.ModelSerializer):
    
    class Meta:
       model = Project 
       fields = ('name','signup')       

    def create(self, validated_data):
        
        instance = super().create(validated_data)
        raw_password = validated_data.get('password')
        instance.set_password(raw_password)
        instance.save()
        return instance


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review 
        fields = ('name','project')

class UploadFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadFiles
        fields = ('file')        

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email').lower()
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError("Please give both email and password.")

        if not Signup.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email does not exist.')
        
        user = authenticate(request=self.context.get('request'), email=email,password=password)
        
        if not user:
            raise serializers.ValidationError("Wrong Credentials.")
        attrs['user']=user      
        return attrs