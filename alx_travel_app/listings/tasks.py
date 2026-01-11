from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_booking_confirmation_email(customer_email, booking_id, trip_name):
    subject = "Booking Confirmation"
    message = f"Dear Customer,\n\nYour booking (ID: {booking_id}) for {trip_name} has been confirmed.\n\nThank you for choosing us!"
    send_mail(
        subject,
        message,
        'mesihgrmay2017@gmail.com',
        [customer_email],
        fail_silently=False,
    )
    return f"Confirmation email sent to {customer_email} for booking {booking_id}"
