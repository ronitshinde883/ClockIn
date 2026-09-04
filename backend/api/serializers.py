from rest_framework import serializers
from .models import College, Department, StudentProfile, TeacherProfile, User,Beacon,AttendanceSession,Attendance

class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = "__all__"

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = [
            "user",
            "division"
        ]

class TeacherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherProfile
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = "__all__"
        
class BeaconSerializer(serializers.ModelSerializer):
    class Meta:
        model=Beacon
        fields="__all__"
        
        
class AttendanceSessionsSerializer(serializers.ModelSerializer):
    class Meta:
        model=AttendanceSession
        fields="__all__"
        
class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = "__all__"
