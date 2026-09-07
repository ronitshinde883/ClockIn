from django.utils import timezone
from rest_framework.exceptions import ValidationError

from .models import Attendance, AttendanceSession

def mark_attendance(student, token):
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

    # if already attendance marked
    if Attendance.objects.filter(
        student=student,
        session=session
    ).exists():
        raise ValidationError("Attendance already marked")

    # create attendance if all checks failed
    attendance = Attendance.objects.create(
        session=session,
        student=student,
        marked_at=timezone.now()
    )

    return attendance