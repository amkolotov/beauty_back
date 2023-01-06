# Generated by Django 4.1.2 on 2023-01-06 10:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('salon', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='Дата обновления')),
                ('name', models.CharField(max_length=128, verbose_name='Наименование')),
                ('img', models.ImageField(upload_to='service_types', verbose_name='Изображение')),
                ('is_publish', models.BooleanField(default=False, verbose_name='Опубликовано')),
            ],
            options={
                'verbose_name': 'Категория услуги',
                'verbose_name_plural': 'Категории услуг',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='Дата обновления')),
                ('name', models.CharField(max_length=128, verbose_name='Наименование')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('is_publish', models.BooleanField(default=False, verbose_name='Опубликовано')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='service.servicecategory', verbose_name='Услуга')),
                ('salons', models.ManyToManyField(related_name='services', to='salon.salon', verbose_name='Салон')),
            ],
            options={
                'verbose_name': 'Услуга',
                'verbose_name_plural': 'Услуги',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='Дата обновления')),
                ('date', models.DateTimeField(verbose_name='Дата бронирования')),
                ('is_confirmed', models.BooleanField(default=False, verbose_name='Подтверждена')),
                ('is_canceled', models.BooleanField(default=False, verbose_name='Отменена')),
                ('is_completed', models.BooleanField(default=False, verbose_name='Выполнена')),
                ('salon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='salon_orders', to='salon.salon', verbose_name='Салон')),
                ('service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='service_orders', to='service.service', verbose_name='Услуга')),
                ('spec', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='spec_orders', to='salon.specialist', verbose_name='Cпециалист')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Заявка',
                'verbose_name_plural': 'Заявки',
                'ordering': ['user'],
            },
        ),
    ]
