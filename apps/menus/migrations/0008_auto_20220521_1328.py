# Generated by Django 3.2.9 on 2022-05-21 13:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('menus', '0007_day_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='is_for_all',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='dish',
            name='user',
            field=models.OneToOneField(
                null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
