from django.urls import path, include
from .views import StudentViewSet, home, CollegeViewSet, DepartmentViewSet, TeacherViewSet, UserCreateViewSet, CreateAttendanceSessionView, MarkAttendanceView, StudentAttendanceView, TeacherSessionAttendanceView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from rest_framework.routers import DefaultRouter

# Register API resources and expose authentication and attendance endpoints.
router = DefaultRouter()

router.register(
    r"students",
    StudentViewSet,
    basename="student"
)

router.register(
    r"teachers",
    TeacherViewSet,
    basename="teacher"
)

router.register(
    r"colleges",
    CollegeViewSet,
    basename="college"
)

router.register(
    r"departments",
    DepartmentViewSet,
    basename="department"
)

urlpatterns = [
    path("", include(router.urls)),
    path("register/", UserCreateViewSet.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login" ),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh" ),
    path("session/", CreateAttendanceSessionView.as_view(), name="session"),
    path("attendance/mark/<uuid:token>/", MarkAttendanceView.as_view(), name="mark_attendance"),
    path("attendance/student", StudentAttendanceView.as_view(), name="student_attendance"),
    path("session/<int:session_id>/attendance/", TeacherSessionAttendanceView.as_view(), name="teacher_session_attendace"),
    path("", home)
]
