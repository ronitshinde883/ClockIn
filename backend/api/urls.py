from django.urls import path, include
from .views import StudentViewSet, home, CollegeViewSet, DepartmentViewSet, TeacherViewSet
from rest_framework.routers import DefaultRouter

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
    path("api/", include(router.urls)),
    path("", home)
]
