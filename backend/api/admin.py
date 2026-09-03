from django.contrib import admin
from api.models import User,StudentProfile,TeacherProfile,Department,College

# Register your models here.
admin.site.register(User)
admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)
admin.site.register(Department)
admin.site.register(College)

