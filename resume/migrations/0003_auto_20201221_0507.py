# Generated by Django 3.1.4 on 2020-12-20 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0002_auto_20201219_0555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personaldetails',
            name='email_address',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='personaldetails',
            name='first_name',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='personaldetails',
            name='last_name',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
