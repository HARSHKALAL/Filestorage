from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework import viewsets
from .models import *
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken
from knox import views as knox_views
from knox.auth import TokenAuthentication
from django.contrib.auth import login
from knox.views import LoginView as KnoxLoginView
from rest_framework.permissions import IsAuthenticated

class RegistrationApi(APIView):

    permission_classes = [IsAuthenticated]       
    def get(self,request): 
        queryset = Signup.objects.filter(id=request.user.id)
        serializer = RegisterSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"userCreated": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"errors":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ProjectApi(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]       

class ReviewAPi(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class LoginAPIView(knox_views.LoginView):
    permission_classes = (AllowAny, )
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)                
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            login(request, user)    
            response = super().post(request,format=None)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        # response.data['user']= serializer.data['email']
        return Response(response.data,status=status.HTTP_200_OK)
