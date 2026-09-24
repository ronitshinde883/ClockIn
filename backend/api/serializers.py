from rest_framework import serializers
from .models import College, Department, StudentProfile, TeacherProfile, User,Beacon,AttendanceSession,Attendance

'''Serialize college records for API input and output.'''
class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = "__all__"

'''Serialize department records for API input and output.'''
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"

'''Serialize student profiles and prevent teacher profile conflicts.'''
class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = "__all__"

    def validate_user(self,user):#cannot register if already teacher
        if TeacherProfile.objects.filter(user=user).exists():
            raise serializers.ValidationError(
                "This user is already registered as a teacher and cannot register as a student."
            )
        return user

'''Serialize teacher profiles and prevent student profile conflicts.'''
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

'''Validate user registration data and create users securely.'''
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
        if User.objects.filter(email=value).exists():
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
        
'''Serialize beacons while enforcing unique beacon UUIDs.'''
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

# attendance session serializer
'''Serialize attendance sessions while protecting generated fields.'''
class AttendanceSessionsSerializer(serializers.ModelSerializer):
    class Meta:
        model=AttendanceSession
        fields="__all__"
        read_only_fields=[
            "teacher",
            "started_at",
            "session_token"
        ]

# attendance serializer
'''Serialize attendance records for API requests and responses.'''
class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = "__all__"

# serializer to view the history of the student attendance marking
'''Present a student's attendance history in a readable format.'''
class StudentAttendanceSerializer(serializers.ModelSerializer):
    subject = serializers.CharField(
        source="session.subject_name",
        read_only= True
    )

    session_date = serializers.DateTimeField(
        source="session.started_at",
        read_only=True
    )

    class Meta:
        model = Attendance
        fields = [
            "id",
            "subject",
            "session_date",
            "marked_at"
        ]

class TeacherAttendanceSerializer(serializers.ModelSerializer):

    student_name = serializers.CharField(
        source="student.user.username",
        read_only=True
    )

    enrollment_no = serializers.CharField(
        sources="student.enrollment_no",
        read_only=True
    )

    marked_time = serializers.DateTimeField(
        sources="marked_at",
        read_only=True
    )

    class Meta:
        model = Attendance
        fields = [
            "id",
            "username",
            "enrollment_no",
            "marked_time"
        ]