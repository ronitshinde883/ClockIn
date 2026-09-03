from rest_framework import serializers
from .models import College, Department, StudentProfile, TeacherProfile, User

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
        model = College
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = "__all__"