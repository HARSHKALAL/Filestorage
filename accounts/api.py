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
    permission_classes = [IsAuthenticated]   
    serializer_class  = ProjectSerializer
    queryset = Project.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data.dict()
        data.update({"signup": request.user.id})
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(Project.objects.filter(signup_id=request.user.id))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ReviewAPi(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(Review.objects.filter(project_id=int(request.GET.get('project'))))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



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
        return Response(response.data,status=status.HTTP_200_OK)
