from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
import uuid ##universally unique indentifier

'''Store the institution details used by departments and users.'''
class College(models.Model):
    name=models.CharField(max_length=200)
    code=models.CharField(max_length=50,unique=True)
    email=models.EmailField()
    address=models.TextField()
    joined_at=models.DateTimeField(auto_now_add=True)
    ##end date will be discussed
    def __str__(self):
        return self.name
    
'''Represent an academic department belonging to a college.'''
class Department(models.Model):
    college=models.ForeignKey(
        College,on_delete=models.CASCADE
    )
    name=models.CharField(max_length=200)
    def __str__(self):
        return self.name
    
    
'''Extend Django users with application-specific role information.'''
class User(AbstractUser):
    ROLE_CHOICES=(
        ("ADMIN","Admin"),
        ("TEACHER","Teacher"),
        ("STUDENT","Student"),
    )
    role=models.CharField(max_length=20,choices=ROLE_CHOICES)

    def __str__(self):
        return self.username
    
    
'''Store enrollment and academic details for a student user.'''
class StudentProfile(models.Model):
    user=models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    college=models.ForeignKey(
        College,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    department=models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    enrollment_no=models.CharField(
        max_length=50,
        unique=True
    )
    division=models.CharField(max_length=20)
    
    def clean(self):
        if TeacherProfile.objects.filter(user=self.user).exists():
            raise ValidationError(
                "This user is already registered as a teacher."
            )
    
    def __str__(self):
        return self.user.username
    
'''Store employment and approval details for a teacher user.'''
class TeacherProfile(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
        )
    user=models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    college=models.ForeignKey(
        College,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    department=models.ForeignKey(
        Department,
        on_delete=models.CASCADE
    )
    employee_id=models.CharField(
        max_length=20,
        unique=True
    )
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='PENDING')
    
    def clean(self):
        if StudentProfile.objects.filter(user=self.user).exists():
            raise ValidationError(
                "This user is already registered as a student."
            )
    def __str__(self):
        return self.user.username

'''Represent a teacher's time-limited attendance session and QR token.'''
class AttendanceSession(models.Model):
    teacher=models.ForeignKey(
        TeacherProfile,
        on_delete=models.CASCADE
    )
    department=models.ForeignKey(
        Department,
        on_delete=models.CASCADE
    )
    subject_name=models.CharField(
        max_length=200,
    )
    session_token=models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )
    started_at=models.DateTimeField(
        auto_now_add=True,
    )
    expires_at=models.DateTimeField()
    is_active=models.BooleanField(default=True)


'''Record one student's attendance in a specific session.'''
class Attendance(models.Model):
    
    session=models.ForeignKey(
        AttendanceSession,
        on_delete=models.CASCADE,
    )
    student=models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
    )
    marked_at=models.DateTimeField(
        auto_now_add=True,
    )
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["session", "student"],
                name="unique_student_session_attendance"
            )
        ]#one student 1 attendance
    
    def __str__(self):
        return self.student.user.username
    
'''Store a named physical beacon associated with a college.'''
class Beacon(models.Model):
    college=models.ForeignKey(
        College,
        on_delete=models.CASCADE
    )
    name=models.CharField(max_length=100)
    uuid=models.CharField(max_length=100)
    
    def __str__(self):
        return self.name