from django.contrib import admin
from api.models import User,StudentProfile,TeacherProfile,Department,College,AttendanceSession,Beacon,Attendance

# Register your models here.
admin.site.register(User)
admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)
admin.site.register(Department)
admin.site.register(College)
admin.site.register(AttendanceSession)
admin.site.register(Beacon)
admin.site.register(Attendance)

