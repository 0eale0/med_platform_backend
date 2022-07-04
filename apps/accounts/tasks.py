from django.core.mail import EmailMessage
from sentry_sdk import capture_message

from django.conf import settings
from med_communication_platform.celery import app


# @app.task()
def send_email_activation(user_email, email_subject, email_text):

    email = EmailMessage(email_subject, email_text, settings.EMAIL_HOST_USER, [user_email])

    email.fail_silently = False
    email.send()

    capture_message(f'Отправлено письмо с текстом {email_text}')


# @app.task()
def test():
    capture_message('OK')
