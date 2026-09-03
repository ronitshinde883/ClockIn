from rest_framework import serializers
from .models import College, Department, StudentProfile, TeacherProfile, User

class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = "__all__"