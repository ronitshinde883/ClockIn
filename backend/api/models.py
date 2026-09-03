from django.db import models
from django.contrib.auth.models import AbstractUser

class College(models.Model):
    name=models.CharField(max_length=200)
    code=models.CharField(max_length=50,unique=True)
    email=models.EmailField()
    address=models.TextField()
    joined_at=models.DateTimeField(auto_now_add=True)
    ##end date will be discussed
    def __str__(self):
        return self.name
    
class Department(models.Model):
    college=models.ForeignKey(
        College,on_delete=models.CASCADE
    )
    name=models.CharField(max_length=200)
    def __str__(self):
        return self.name
    
    
class User(AbstractUser):
    ROLE_CHOICES=(
        ("ADMIN","Admin"),
        ("TEACHER","Teacher"),
        ("STUDENT","Student"),
    )
    role=models.CharField(max_length=20,choices=ROLE_CHOICES)
    college=models.ForeignKey(
        College,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    
    def __str__(self):
        return self.username
    
    
class StudentProfile(models.Model):
    user=models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    department=models.ForeignKey(
        Department,
        on_delete=models.CASCADE
    )
    enrollment_no=models.CharField(
        max_length=50,
        unique=True
    )
    division=models.CharField(max_length=20)
    
    def __str__(self):
        return self.user.username
    
class TeacherProfile(models.Model):
    user=models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    department=models.ForeignKey(
        Department,
        on_delete=models.CASCADE
    )
    employee_id=models.CharField(
        max_length=20,
        unique=True
    )
    def __str__(self):
        return self.user.username
