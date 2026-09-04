from rest_framework import viewsets
from django.shortcuts import render,HttpResponse
from .models import StudentProfile, TeacherProfile, College, Department,Beacon,AttendanceSession,Attendance
from .serializers import StudentProfileSerializer, TeacherProfileSerializer, CollegeSerializer, DepartmentSerializer,BeaconSerializer,AttendanceSessionsSerializer,AttendanceSerializer
# Create your views here.
def home(request):
   return HttpResponse("RONIT CHAKKA HAI")

class StudentViewSet(viewsets.ModelViewSet):
   queryset = StudentProfile.objects.all()
   serializer_class = StudentProfileSerializer

class TeacherViewSet(viewsets.ModelViewSet):
   queryset = TeacherProfile.objects.all()
   serializer_class = TeacherProfileSerializer

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
   
class AttendanceViewSet(viewsets.ModelViewSet):
   queryset=Attendance.objects.all()
   serializer_class=AttendanceSerializer
   
   
