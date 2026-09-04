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

    def validate_user(self,user):#cannot register if already teacher
        if TeacherProfile.objects.filter(user=user):
            raise serializers.ValidationError(
                "This user is already registered as a teacher and cannot register as a student."
            )
        return user

class TeacherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherProfile
        fields = "__all__"
        
    def validate_user(self,user):
        if StudentProfile.objects.filter(user=user).exists():
            raise serializers.ValidationError(
                "This user is already registered as a student and cannot register as a teacher."
            )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "role"
        ]
        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }
    def validate_email(self,value):
        if User.objects.filter(email=value).exist():
            raise serializers.ValidationError(
                "This email is already registered"
            )
        return value
        
    def validate_username(self,value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "This username is already taken."
            )
        return value
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
        
class BeaconSerializer(serializers.ModelSerializer):
    class Meta:
        model=Beacon
        fields="__all__"
        
    def validate_uuid(self,value):
        if Beacon.objects.filter(uuid=value):
            raise serializers.ValidationError(
                "A beacon with this UUID already exists."
            )     
        return value
    
class AttendanceSessionsSerializer(serializers.ModelSerializer):
    class Meta:
        model=AttendanceSession
        fields="__all__"
    
class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = "__all__"
