from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

@shared_task
def send_email_verfication(subject, message, email_to):
    """ send email to candidates and organizations """
    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=[email_to]
        )
        email.content_subtype = 'html'
        email.mixed_subtype = 'related'
        email.send()
    except Exception as e:
        print(e)
        pass
