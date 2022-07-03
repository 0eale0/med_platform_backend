from uuid import uuid4

from django.urls import reverse

from apps.accounts.tasks import send_email_activation


def send_activate_user_email(domain, user_email, email_token):
    view_name = "VerifyEmail"
    url_path = reverse(view_name, kwargs={'token': email_token})

    activate_url = f"{domain}{url_path}"
    email_subject = "Активируйте ваш аккаунт"
    email_text = f"Пожалуйста, для активации вашего аккаунта, пройдите по ссылке \n{activate_url}"

    send_email_activation(user_email, email_subject, email_text)


def send_reset_password_email(domain, user_email, password_token):
    view_name = "ResetPassword"
    url_path = reverse(view_name, kwargs={'token': password_token})

    activate_url = f"{domain}{url_path}"
    email_subject = "Сброс пароля"
    email_text = f"Пожалуйста, для сброса вашего пароля, пройдите по ссылке \n{activate_url}"

    send_email_activation(user_email, email_subject, email_text)