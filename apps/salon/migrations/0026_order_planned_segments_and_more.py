# Generated by Django 4.1.2 on 2023-04-20 14:05

import apps.auth_app.validators
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
        ('salon', '0025_remove_order_segments_order_end_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='planned_segments',
            field=models.ManyToManyField(related_name='orders', to='schedule.plannedsegment'),
        ),
        migrations.AlterField(
            model_name='companyinfo',
            name='work_time_end',
            field=models.TimeField(default=datetime.time(20, 0), validators=[apps.auth_app.validators.validate_time], verbose_name='Время окончания работы'),
        ),
        migrations.AlterField(
            model_name='companyinfo',
            name='work_time_start',
            field=models.TimeField(default=datetime.time(10, 0), validators=[apps.auth_app.validators.validate_time], verbose_name='Время начала работы'),
        ),
        migrations.AlterField(
            model_name='order',
            name='end_time',
            field=models.TimeField(validators=[apps.auth_app.validators.validate_time], verbose_name='Время окончания'),
        ),
        migrations.AlterField(
            model_name='order',
            name='start_time',
            field=models.TimeField(validators=[apps.auth_app.validators.validate_time], verbose_name='Время начала'),
        ),
        migrations.AlterField(
            model_name='salon',
            name='work_time_end',
            field=models.TimeField(default=datetime.time(20, 0), validators=[apps.auth_app.validators.validate_time], verbose_name='Время окончания работы'),
        ),
        migrations.AlterField(
            model_name='salon',
            name='work_time_start',
            field=models.TimeField(default=datetime.time(10, 0), validators=[apps.auth_app.validators.validate_time], verbose_name='Время начала работы'),
        ),
    ]