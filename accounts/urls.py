from django.urls import path
from .views import *
from .api import *

urlpatterns = [
    path("api/register/",RegistrationApi.as_view(),name='RegistrationApi'),   
    path("api/project/",ProjectApi.as_view(),name='ProjectApi'),   
    path("api/review/",ReviewAPi.as_view(),name='ReviewApi'), 
    path("api/login/", LoginAPIView.as_view(),name='knox_login'),
]

templates_urlpatterns = [
    path("homepage/",homepage,name="homepage"),
    path("register/",register,name="register"),
    path("signin/",signin,name="signin"),
]

urlpatterns += templates_urlpatterns

