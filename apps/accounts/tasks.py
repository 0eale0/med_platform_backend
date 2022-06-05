from django.core.mail import EmailMessage
from django.urls import reverse
from sentry_sdk import capture_message

from med_communication_platform import settings
from med_communication_platform.celery import app


@app.task()
def send_email_activation(domain, user_email, email_token):

    activate_url = f'http://med-plaform.a.uenv.ru/verify/{email_token}/'

    email_subject = "Активируйте ваш аккаунт"
    email_text = f"Пожалуйста, для активации вашего аккаунт, пройдите по ссылке \n{activate_url}"

    email = EmailMessage(email_subject, email_text, settings.EMAIL_HOST_USER, [user_email])

    email.fail_silently = False
    email.send()
    capture_message(f'Отправлено письмо с ссылкой {activate_url}')


@app.task()
def test():
    capture_message('OK')
