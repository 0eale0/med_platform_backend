# Generated by Django 3.2.9 on 2021-12-03 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_alter_user_middle_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="patient",
            name="link_token",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
