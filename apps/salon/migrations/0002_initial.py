# Generated by Django 4.1.2 on 2023-01-06 10:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('service', '0001_initial'),
        ('salon', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='specialist',
            name='services',
            field=models.ManyToManyField(related_name='specialists', to='service.servicecategory', verbose_name='Услуги'),
        ),
        migrations.AddField(
            model_name='salonimg',
            name='salon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='salon_imgs', to='salon.salon', verbose_name='Салон'),
        ),
        migrations.AddField(
            model_name='sale',
            name='salons',
            field=models.ManyToManyField(related_name='sales', to='salon.salon', verbose_name='Салоны'),
        ),
        migrations.AddField(
            model_name='review',
            name='salon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='salon_reviews', to='salon.salon', verbose_name='Салон'),
        ),
        migrations.AddField(
            model_name='review',
            name='spec',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='spec_reviews', to='salon.specialist', verbose_name='Специалист'),
        ),
        migrations.AddField(
            model_name='review',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
