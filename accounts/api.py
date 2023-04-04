from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer,ProjectSerializer,ReviewSerializer,LoginSerializer,UploadFilesSerializer
from .models import Signup,Project,Review,UploadFiles
from rest_framework import generics
from knox import views as knox_views
from django.contrib.auth import login
from rest_framework.permissions import IsAuthenticated,AllowAny


class RegistrationApi(APIView):       
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
        queryset = self.filter_queryset(Review.objects.filter(project_id =self.request.query_params.get('project')))
        serializer = self.get_serializer(queryset,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UploadFileApi(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = UploadFilesSerializer


class LoginAPIView(knox_views.LoginView):
                                                   
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)                
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            login(request, user)    
            response = super().post(request,format=None)
        else:            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(response.data,status=status.HTTP_200_OK)
