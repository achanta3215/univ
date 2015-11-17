from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser,UserManager
from django.contrib.auth import get_user_model
# Create your models here.


class Department(models.Model):
    dname = models.CharField(max_length=200,primary_key=True)
    
    def publish(self):
        self.save()
        
    def __str__(self):
        return self.dname
    
class UserAugment(AbstractUser):
     department = models.ForeignKey(Department,null=True,blank=True)
     objects = UserManager()
     def is_superuser():
        user = get_user_model()
        x = UserAugment.objects.values_list('is_superuser').filter(username=user)
        return x

class Student(models.Model):
    sname = models.CharField(max_length=200)
    usn = models.CharField(max_length=200,primary_key=True)
    dept = models.ForeignKey(Department)
    sem = models.IntegerField()
    
    def publish(self):
        self.save()
        
    def __str__(self):
        return self.usn

class Course(models.Model):
    cname = models.CharField(max_length=200)
    code = models.CharField(max_length=200,primary_key=True)
    dname = models.ForeignKey(Department)
    sem = models.IntegerField()
    
    def publish(self):
        self.save()
        
    def __str__(self):
        return self.code
    
class Result(models.Model):
    usn = models.ForeignKey(Student)
    course = models.ForeignKey(Course)
    intmarks = models.IntegerField()
    extmarks = models.IntegerField()
    
    class Meta:
        unique_together = ("usn", "course")
    
    def publish(self):
        self.save()
    def __str__(self):
        return self.usn.usn

    
