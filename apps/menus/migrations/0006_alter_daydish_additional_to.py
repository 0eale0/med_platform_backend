# Generated by Django 3.2.9 on 2022-04-06 17:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0005_auto_20220404_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daydish',
            name='additional_to',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='menus.daydish'),
        ),
    ]
