from django.core.mail import EmailMessage
from django.urls import reverse
from sentry_sdk import capture_message

from med_communication_platform import settings
from med_communication_platform.celery import app


@app.task()
def send_email_activation(domain, user_email, email_token):
    link = reverse('VerifyEmail', kwargs={'token': email_token})
    activate_url = 'http://' + domain + link

    email_subject = "Activate you're account"
    email_text = f"Please the link below to activate your account \n{activate_url}"

    email = EmailMessage(email_subject, email_text, settings.EMAIL_HOST_USER, [user_email])

    email.fail_silently = False
    email.send()


@app.task()
def test():
    capture_message('OK')
