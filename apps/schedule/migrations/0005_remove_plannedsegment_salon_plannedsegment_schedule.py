# Generated by Django 4.1.2 on 2023-04-24 12:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0004_plannedsegment_salon_alter_schedule_break_time_end_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plannedsegment',
            name='salon',
        ),
        migrations.AddField(
            model_name='plannedsegment',
            name='schedule',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='planned_segments', to='schedule.schedule', verbose_name='Дневное расписание'),
            preserve_default=False,
        ),
    ]