# Generated by Django 3.0.5 on 2020-12-14 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CartApp', '0005_customer_profile_pic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='profile_pic',
        ),
    ]
