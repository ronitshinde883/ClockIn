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
)
from .permissions import IsAdmin, IsStudent, IsTeacher, IsTeacherOrAdmin
from .services import mark_attendance


# Create your views here.
def home(request):
    return HttpResponse("RONIT CHAKKA HAI")


class StudentViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated]


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherProfileSerializer
    permission_classes = [IsAuthenticated]


class CollegeViewSet(viewsets.ModelViewSet):
    queryset = College.objects.all()
    serializer_class = CollegeSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class BeaconViewSet(viewsets.ModelViewSet):
    queryset = Beacon.objects.all()
    serializer_class = BeaconSerializer


class AttendanceSessionsViewSet(viewsets.ModelViewSet):
    queryset = AttendanceSession.objects.all()
    serializer_class = AttendanceSessionsSerializer
    permission_classes = [IsAuthenticated]


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]


class UserCreateViewSet(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


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