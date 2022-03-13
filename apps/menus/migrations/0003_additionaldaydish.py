# Generated by Django 3.2.9 on 2022-03-13 21:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0002_daydish_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalDayDish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('additional_day_dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='additional_day_dish', to='menus.daydish')),
                ('main_day_dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_day_dish', to='menus.daydish')),
            ],
        ),
    ]
