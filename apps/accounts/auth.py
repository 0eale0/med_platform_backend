from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from six import text_type

from med_communication_platform import settings


class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return text_type(user.is_active) + text_type(user.pk) + text_type(timestamp)


account_activation_token = AppTokenGenerator()


def send_email_activation(request, user):
    domain = get_current_site(request).domain
    uid_64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)

    link = reverse('VerifyEmail', kwargs={'uid_64': uid_64, 'token': token})
    activate_url = 'http://' + domain + link

    email_subject = "Activate you're account"
    email_text = f"Please the link below to activate your account \n{activate_url}"
    user_email = user.email

    email = EmailMessage(email_subject, email_text, settings.EMAIL_HOST_USER, [user_email])

    email.fail_silently = False
    email.send()


class UserProfileManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email)

        user.username = email
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)
        return user
