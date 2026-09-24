from datetime import timedelta

from django.shortcuts import render, HttpResponse
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated

from .models import (
    StudentProfile,
    TeacherProfile,
    College,
    Department,
    Beacon,
    AttendanceSession,
    Attendance,
    User,
)
from .serializers import (
    StudentProfileSerializer,
    TeacherProfileSerializer,
    CollegeSerializer,
    DepartmentSerializer,
    BeaconSerializer,
    AttendanceSessionsSerializer,
    AttendanceSerializer,
    UserSerializer,
    StudentAttendanceSerializer
)
from .permissions import IsAdmin, IsStudent, IsTeacher, IsTeacherOrAdmin
from .services import mark_attendance


# Create your views here.
def home(request):
    '''Return the basic response for the application home endpoint.'''
    return HttpResponse("RONIT CHAKKA HAI")

"""
student view set includes endpoints like:
GET     /students/      list
POST    /students/      create
GET     /students/{id}  retrieve
PUT     /students/{id}  update
PATCH   /students/{id}  partial_update
DELETE  /students/{id}  delete/destroy
"""
class StudentViewSet(viewsets.ModelViewSet):
    '''Provide CRUD endpoints for student profiles.'''
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated]

"""
teacher view set includes endpoints like:
GET     /teachers/      list
POST    /teachers/      create
GET     /teachers/{id}  retrieve
PUT     /teachers/{id}  update
PATCH   /teachers/{id}  partial_update
DELETE  /teachers/{id}  delete/destroy
"""
class TeacherViewSet(viewsets.ModelViewSet):
    '''Provide CRUD endpoints for teacher profiles.'''
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherProfileSerializer
    permission_classes = [IsAuthenticated]

"""
college view set includes endpoints like:
GET     /colleges/      list
POST    /colleges/      create
GET     /colleges/{id}  retrieve
PUT     /colleges/{id}  update
PATCH   /colleges/{id}  partial_update
DELETE  /colleges/{id}  delete/destroy
"""
class CollegeViewSet(viewsets.ModelViewSet):
    '''Provide CRUD endpoints for colleges.'''
    queryset = College.objects.all()
    serializer_class = CollegeSerializer

"""
department view set includes endpoints like:
GET     /departments/      list
POST    /departments/      create
GET     /departments/{id}  retrieve
PUT     /departments/{id}  update
PATCH   /departments/{id}  partial_update
DELETE  /departments/{id}  delete/destroy
"""
class DepartmentViewSet(viewsets.ModelViewSet):
    '''Provide CRUD endpoints for departments.'''
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class BeaconViewSet(viewsets.ModelViewSet):
    '''Provide CRUD endpoints for registered beacons.'''
    queryset = Beacon.objects.all()
    serializer_class = BeaconSerializer


class AttendanceSessionsViewSet(viewsets.ModelViewSet):
    '''Provide authenticated CRUD endpoints for attendance sessions.'''
    queryset = AttendanceSession.objects.all()
    serializer_class = AttendanceSessionsSerializer
    permission_classes = [IsAuthenticated]


class AttendanceViewSet(viewsets.ModelViewSet):
    '''Provide authenticated CRUD endpoints for attendance records.'''
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

"""
this view set includes endpoints like:
POST  /register/   JSON data-> user creation
"""
class UserCreateViewSet(generics.CreateAPIView):
    '''Provide the user registration endpoint.'''
    queryset = User.objects.all()
    serializer_class = UserSerializer

"""
create attendance session view used to create a session by teachers
includes validation
teacher login validation,
role based access so that only users with the role teacher can create the session
department validation if it exists or not
also sessions can be only created if the teacher belongs to that department
"""
class CreateAttendanceSessionView(APIView):
    '''Create a time-limited attendance session for a teacher's department.'''
    permission_classes = [IsTeacher]

    def post(self, request):
        subject_name = request.data.get("subject")
        department_id = request.data.get("department")

        if not subject_name or not department_id:
            return Response(
                {"error": "Subject name and department id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        # check if teacher profile already exists
        try:
            teacher = TeacherProfile.objects.get(user=request.user)
        except TeacherProfile.DoesNotExist:
            return Response(
                {"error": "Teacher profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # check if department actually exists
        try:
            department = Department.objects.get(id=department_id)
        except Department.DoesNotExist:
            return Response(
                {"error" : "Department not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # check if teacher have access to this department
        if teacher.department != department:
            return Response(
                {"error": "You cannot create a session for this department"},
                status=status.HTTP_403_FORBIDDEN
            )

        # create session
        session = AttendanceSession.objects.create(
            teacher=teacher,
            department=department,
            subject_name=subject_name,
            expires_at=timezone.now() + timedelta(minutes=30),
            is_active=True,
        )

        serializer = AttendanceSessionsSerializer(session)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
"""
marks attendance of the student
includes validation like if the user is logged in or not
and if the session is active or expired
all the validation logic is included in the service mark_attendance
"""
class MarkAttendanceView(APIView):
    '''Mark attendance for an authenticated student using a QR token.'''
    permission_classes=[IsStudent]

    def post(self, request, token):

        print("========== ATTENDANCE REQUEST ==========")
        print("TOKEN:", token)
        print("USER:", request.user)
        print("ROLE:", request.user.role)
        print("METHOD:", request.method)
        print("========================================")
        if not token:
            return Response(
                {"error": "QR token is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        attendance = mark_attendance(
            student=request.user.studentprofile,
            token=token
        )

        return Response(
            {
                "message": "Attendance marked successfully",
                "attendance_id": attendance.id
            },
            status=status.HTTP_201_CREATED
        )

"""
view to check the history of the attendances marked by students
checks if the user is a student
queries the database for attendance records and are arranged according to the marked_at datetime format
"""
class StudentAttendanceView(APIView):
    '''Return the authenticated student's attendance history.'''
    permission_classes = [IsStudent]

    def get(self, request):
        try:
            student = StudentProfile.objects.get(
                user=request.user
            )
        except StudentProfile.DoesNotExist:
            return Response(
                {"error": "The student profile for this user does not exists"},
                status=status.HTTP_404_NOT_FOUND
            )

        attendance = Attendance.objects.filter(
            student = student
        ).select_related("session").order_by("-marked_at")

        serializer = StudentAttendanceSerializer(
            attendance, 
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )