from datetime import timedelta

from django.shortcuts import render,HttpResponse
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated

from .models import StudentProfile, TeacherProfile, College, Department,Beacon,AttendanceSession,Attendance, User
from .serializers import StudentProfileSerializer, TeacherProfileSerializer, CollegeSerializer, DepartmentSerializer,BeaconSerializer,AttendanceSessionsSerializer,AttendanceSerializer, UserSerializer
from .permissions import IsAdmin, IsStudent, IsTeacher, IsTeacherOrAdmin



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
   queryset=Beacon.objects.all()
   serializer_class=BeaconSerializer
   
class AttendanceSessionsViewSet(viewsets.ModelViewSet):
   queryset=AttendanceSession.objects.all()
   serializer_class=AttendanceSessionsSerializer
   permission_classes = [IsAuthenticated]
   
class AttendanceViewSet(viewsets.ModelViewSet):
   queryset=Attendance.objects.all()
   serializer_class=AttendanceSerializer
   permission_classes = [IsAuthenticated]
   
class UserCreateViewSet(generics.CreateAPIView):
   queryset = User.objects.all()
   serializer_class = UserSerializer


class CreateAttendanceSessionView(APIView):
   permission_classes = [IsTeacher]

   def post(self, request):
      subject_name = request.data.get("subject")
      department_id = request.data.get("department")

      if not subject_name:
         return Response(
            {"error": "Subject name or department field missing"},
            status=status.HTTP_400_BAD_REQUEST
         )

      teacher = request.user.teacherprofile

      session = AttendanceSession.objects.create(
         teacher=teacher,
         subject_name=subject_name,
         department_id=department_id,
         expires_at=timezone.now() + timedelta(seconds=30),
         is_active=True
      )

      serializer = AttendanceSessionsSerializer(session)

      return Response(
         serializer.data,
         status=status.HTTP_201_CREATED
      )
