# Generated by Django 3.2.9 on 2021-12-04 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_patient_link_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='link_token',
            field=models.CharField(default='0', max_length=100),
            preserve_default=False,
        ),
    ]
