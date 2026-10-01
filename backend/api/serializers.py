from rest_framework import serializers
from .models import (
    College,
    Department,
    StudentProfile,
    TeacherProfile,
    User,
    AttendanceSession,
    Attendance,
)

"""Serialize college records for API input and output."""


class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = "__all__"


"""Serialize department records for API input and output."""


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


"""Serialize student profiles and prevent teacher profile conflicts."""


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = "__all__"

    def validate_user(self, user):  # cannot register if already teacher
        if TeacherProfile.objects.filter(user=user).exists():
            raise serializers.ValidationError(
                "This user is already registered as a teacher and cannot register as a student."
            )
        return user


"""Serialize teacher profiles and prevent student profile conflicts."""


class TeacherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherProfile
        fields = "__all__"

    def validate_user(self, user):
        if StudentProfile.objects.filter(user=user).exists():
            raise serializers.ValidationError(
                "This user is already registered as a student and cannot register as a teacher."
            )
        return user


"""Validate user registration data and create users securely."""


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "role"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


# attendance session serializer
"""Serialize attendance sessions while protecting generated fields."""


class AttendanceSessionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceSession
        fields = "__all__"
        read_only_fields = ["teacher", "started_at", "session_token"]


# attendance serializer
"""Serialize attendance records for API requests and responses."""


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = "__all__"


# serializer to view the history of the student attendance marking
"""Present a student's attendance history in a readable format."""


class StudentAttendanceSerializer(serializers.ModelSerializer):
    subject = serializers.CharField(source="session.subject_name", read_only=True)

    session_date = serializers.DateTimeField(
        source="session.started_at", read_only=True
    )

    class Meta:
        model = Attendance
        fields = ["id", "subject", "session_date", "marked_at"]


class TeacherAttendanceSerializer(serializers.ModelSerializer):

    student_name = serializers.CharField(source="student.user.username", read_only=True)

    enrollment_no = serializers.CharField(
        source="student.enrollment_no", read_only=True
    )

    marked_time = serializers.DateTimeField(source="marked_at", read_only=True)

    class Meta:
        model = Attendance
        fields = ["id", "username", "enrollment_no", "marked_time"]


# student register serializer, to register a studentprofile whilst also creating an user at the same time
class StudentRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = StudentProfile

        fields = [
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "college",
            "department",
            "enrollment_no",
            "division",
        ]

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")

        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered.")

        return value

    def validate(self, attrs):
        if attrs["department"].college_id != attrs["college"].id:
            raise serializers.ValidationError(
                {
                    "department": "This department does not belong to the selected college"
                }
            )

        return attrs


# teacher register seriazlier, to register a teacherprofile whilst also creating an user at the same time
class TeacherRegisterSerializer(serializers.ModelSerializer):

    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = TeacherProfile
        fields = [
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "college",
            "department",
            "employee_id",
        ]

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")

        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered.")

        return value

    def validate(self, attrs):
        if attrs["department"].college_id != attrs["college"].id:
            raise serializers.ValidationError(
                {
                    "department": "This department does not belong to the selected college."
                }
            )

        return attrs


class StudentResponseSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source="user.username")

    first_name = serializers.CharField(source="user.first_name")

    last_name = serializers.CharField(source="user.last_name")

    email = serializers.EmailField(source="user.email")

    date_joined = serializers.DateTimeField(source="user.date_joined")

    last_login = serializers.DateTimeField(source="user.last_login")

    is_active = serializers.BooleanField(source="user.is_active")

    role = serializers.CharField(source="user.role")

    class Meta:
        model = StudentProfile
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "date_joined",
            "last_login",
            "is_active",
            "role",
            "college",
            "department",
            "enrollment_no",
            "division",
        ]


class TeacherResponseSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")

    first_name = serializers.CharField(source="user.first_name")

    last_name = serializers.CharField(source="user.last_name")

    email = serializers.EmailField(source="user.email")

    date_joined = serializers.DateTimeField(source="user.date_joined")

    last_login = serializers.DateTimeField(source="user.last_login")

    is_active = serializers.BooleanField(source="user.is_active")

    role = serializers.CharField(source="user.role")

    class Meta:
        model = TeacherProfile
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "date_joined",
            "last_login",
            "is_active",
            "role",
            "college",
            "department",
            "employee_id",
        ]
