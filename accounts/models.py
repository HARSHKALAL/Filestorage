from django.db import models
from django.contrib.auth.models import AbstractUser
import pathlib
import random

class Signup(AbstractUser):
    username = None
    date_of_birth = models.DateField(null=True)
    email= models.EmailField(unique=True)

    USERNAME_FIELD = 'email'    
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Project(models.Model):
    name = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now_add=True)        
    signup = models.ForeignKey(Signup,on_delete=models.CASCADE,related_name="signupProject")
    
    def __str__(self):
        return self.name

class Review(models.Model):
    name = models.CharField(max_length=100,blank=True,null=True)
    project = models.ForeignKey(Project,on_delete=models.CASCADE,related_name="projectReview")
    date = models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = "Review Step" + str(random.randrange(000,999))
        super(Review, self).save(*args, **kwargs) 



class UploadFiles(models.Model):
    file = models.FileField(upload_to="files/")
    name = models.CharField(max_length=100,blank=True,null=True)
    review = models.ForeignKey(Review,on_delete=models.CASCADE,related_name="reviewUploadfiles")
    date = models.DateTimeField(auto_now_add=True)    
 
    def save(self, *args, **kwargs):
       self.name = pathlib.Path(self.file.path).stem
       super(UploadFiles, self).save(*args, **kwargs) 
    
    def __str__(self):
        return self.name
