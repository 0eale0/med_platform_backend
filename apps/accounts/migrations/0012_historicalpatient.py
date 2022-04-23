# Generated by Django 3.2.9 on 2022-04-23 11:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0006_alter_daydish_additional_to'),
        ('accounts', '0011_auto_20220421_1405'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalPatient',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, max_length=100, null=True)),
                ('medical_card_number', models.CharField(blank=True, max_length=255, null=True)),
                ('insurance_policy_number', models.CharField(blank=True, max_length=100, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('link_token', models.CharField(blank=True, max_length=100, null=True)),
                ('sex', models.CharField(blank=True, choices=[('male', 'male'), ('female', 'female')], max_length=6, null=True)),
                ('activity_level', models.CharField(blank=True, max_length=255, null=True)),
                ('weight', models.FloatField(blank=True, null=True)),
                ('waist', models.FloatField(blank=True, null=True)),
                ('height', models.FloatField(blank=True, null=True)),
                ('hips', models.IntegerField(blank=True, null=True)),
                ('medical_information', models.TextField(blank=True, null=True)),
                ('country', models.CharField(blank=True, max_length=60, null=True)),
                ('city', models.CharField(blank=True, max_length=60, null=True)),
                ('address', models.CharField(blank=True, max_length=60, null=True)),
                ('calories', models.IntegerField(blank=True, null=True)),
                ('protein', models.IntegerField(blank=True, null=True)),
                ('fat', models.IntegerField(blank=True, null=True)),
                ('carbohydrate', models.IntegerField(blank=True, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('doctor', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='accounts.doctor')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('menu', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='menus.menu')),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical patient',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
