from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_auth_email_task(subject, message, from_email, recipient_email):
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=[recipient_email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Error sending email: {e}")
        raise self.retry(countdown=2**self.request.retries, max_retries=3)