from .models import Signup,Project,Review,UploadFiles
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
        fields = "__all__"

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review 
        fields = ('id','name','project')

class UploadFilesSerializer(serializers.ModelSerializer):
    review = ReviewSerializer(read_only=True,many=True)
    name = serializers.CharField(read_only=True)
    class Meta:
        model = UploadFiles
        fields = ('file','name','review')        

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email').lower()
        password = attrs.get('password')

        if not Signup.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email does not exist.')
                
        user = authenticate(request=self.context.get('request'), email=email,password=password)
        
        if not user:
            raise serializers.ValidationError("Enter Valid Password.")
        
        attrs['user']=user      
        return attrs