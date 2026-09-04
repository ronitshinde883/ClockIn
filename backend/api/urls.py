from django.urls import path, include
from .views import StudentViewSet, home, CollegeViewSet, DepartmentViewSet, TeacherViewSet, UserCreateViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
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
    path("api/register/", UserCreateViewSet.as_view(), name="register"),
    path("api/login/", TokenObtainPairView.as_view(), name="login" ),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh" ),
    path("", home)
]
