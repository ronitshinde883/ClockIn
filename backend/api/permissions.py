from rest_framework.permissions import BasePermission

'''Permit API access only for authenticated teacher users.'''
class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "TEACHER"
        )

'''Permit API access only for authenticated student users.'''
class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "STUDENT"
        )

'''Permit API access only for authenticated administrator users.'''
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "ADMIN"
        )

'''Permit API access for authenticated teachers or administrators.'''
class IsTeacherOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.role == "TEACHER" 
                    or request.user.role == "ADMIN"
            )
        )