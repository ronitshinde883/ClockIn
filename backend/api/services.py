from django.utils import timezone
from rest_framework.exceptions import ValidationError

from .utils import calculate_distance
from .models import Attendance, AttendanceSession


'''Validate a QR session token and create the student's attendance.'''
def mark_attendance(student, token, student_latitude, student_longitude):
    # find session using qr token
    try:
        session = AttendanceSession.objects.get(qr_token=token)
    except:
        raise ValidationError("Invalid QR code")

    # check if session is active
    if not session.is_active:
        raise ValidationError("Attendance session is not active")

    # if qr expired or not
    if timezone.now() > session.qr_token_expires_at:
        raise ValidationError("QR code already expired")

    # student belongs to the same department as of the session
    if student.department != session.department:
        raise ValidationError("You are not part of this department")

    # calculate distance of student wrt to teacher
    distance = calculate_distance(
        session.teacher_latitude,
        session.teacher_longitude,
        student_latitude,
        student_longitude
    )   

    # student is within 50m radius
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
