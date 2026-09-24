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
    StudentAttendanceSerializer,
    TeacherAttendanceSerializer
)
from .permissions import IsAdmin, IsStudent, IsTeacher, IsTeacherOrAdmin
from .services import mark_attendance


# Create your views here.
'''Return the basic response for the application home endpoint.'''
def home(request):
    return HttpResponse("WINNER WINNER CHICKEN DINNER...!")

"""
student view set includes endpoints like:
GET     /students/      list
POST    /students/      create
GET     /students/{id}  retrieve
PUT     /students/{id}  update
PATCH   /students/{id}  partial_update
DELETE  /students/{id}  delete/destroy
"""
'''Provide CRUD endpoints for student profiles.'''
class StudentViewSet(viewsets.ModelViewSet):
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
'''Provide CRUD endpoints for teacher profiles.'''
class TeacherViewSet(viewsets.ModelViewSet):
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
'''Provide CRUD endpoints for colleges.'''
class CollegeViewSet(viewsets.ModelViewSet):
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
'''Provide CRUD endpoints for departments.'''
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


'''Provide CRUD endpoints for registered beacons.'''
class BeaconViewSet(viewsets.ModelViewSet):
    queryset = Beacon.objects.all()
    serializer_class = BeaconSerializer


'''Provide authenticated CRUD endpoints for attendance sessions.'''
class AttendanceSessionsViewSet(viewsets.ModelViewSet):
    queryset = AttendanceSession.objects.all()
    serializer_class = AttendanceSessionsSerializer
    permission_classes = [IsAuthenticated]


'''Provide authenticated CRUD endpoints for attendance records.'''
class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

"""
this view set includes endpoints like:
POST  /register/   JSON data-> user creation
"""
'''Provide the user registration endpoint.'''
class UserCreateViewSet(generics.CreateAPIView):
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
'''Create a time-limited attendance session for a teacher's department.'''
class CreateAttendanceSessionView(APIView):
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
'''Mark attendance for an authenticated student using a QR token.'''
class MarkAttendanceView(APIView):
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
'''Return the authenticated student's attendance history.'''
class StudentAttendanceView(APIView):
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

'''Returns the record of students who have marked their attendance to teacher\
    IMPROVEMENT: can be improved using websockets
    '''
class TeacherSessionAttendanceView(APIView):
    permission_classes = [IsTeacher]

    def get(self, request, session_id):

        try:
            teacher = TeacherProfile.objects.get(
                user=request.user
            )
        except TeacherProfile.DoesNotExist:
            return Response(
                {"error": "The teacher profile for this user does not exists"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            session = AttendanceSession.objects.get(
                id = session_id,
                teacher=teacher
            )
        except AttendanceSession.DoesNotExist:
            return Response(
                {"error": "Attendance session not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        attendance = Attendance.objects.filter(
            session = session
        ).select_related("student__user").order_by("marked_at")

        serializer = TeacherAttendanceSerializer(
            attendance,
            many=True
        )

        return Response (
            serializer.data,
            status=status.HTTP_200_OK
        )