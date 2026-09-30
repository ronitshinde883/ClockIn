from django.utils import timezone
from rest_framework.exceptions import ValidationError

from .utils import calculate_distance
from .models import Attendance, AttendanceSession


'''Validate a QR session token and create the student's attendance.'''
def mark_attendance(student, token, student_latitude, student_longitude):
    # find session using qr token
    try:
        session = AttendanceSession.objects.get(session_token=token)
    except:
        raise ValidationError("Invalid QR code")

    # check if session is active
    if not session.is_active:
        raise ValidationError("Attendance session is not active")

    # if expired or not
    if timezone.now() > session.expires_at:
        raise ValidationError("QR already expired")

    if student.department != session.department:
        raise ValidationError("You are not part of this department")

    distance = calculate_distance(
        session.teacher_latitude,
        session.teacher_longitude,
        student_latitude,
        student_longitude
    )

    if distance > 50:
        raise ValidationError("You are too far from the teacher")

    # if already attendance marked
    if Attendance.objects.filter(student=student, session=session).exists():
        raise ValidationError("Attendance already marked")

    # create attendance if all checks failed
    attendance = Attendance.objects.create(
        session=session, 
        student=student, 
        marked_at=timezone.now()
    )

    return attendance
