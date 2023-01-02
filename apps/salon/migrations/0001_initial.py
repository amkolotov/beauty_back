# Generated by Django 4.1.2 on 2023-01-02 12:19

import apps.auth_app.fields
import apps.auth_app.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='Дата обновления')),
                ('name', models.CharField(max_length=128, verbose_name='Наименование')),
                ('logo', models.FileField(upload_to='company', validators=[apps.auth_app.validators.validate_image_and_svg_file_extension], verbose_name='Логотип')),
                ('img', models.ImageField(upload_to='company', verbose_name='Изображение')),
                ('address', models.CharField(blank=True, max_length=128, null=True, verbose_name='Адрес')),
                ('phone', apps.auth_app.fields.PhoneField(blank=True, max_length=20, null=True, verbose_name='Телефон')),
                ('decs', models.TextField(verbose_name='Описание')),
                ('is_publish', models.BooleanField(default=False, verbose_name='Опубликована')),
            ],
            options={
                'verbose_name': 'Компания',
                'verbose_name_plural': 'Компания',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='Дата обновления')),
                ('rating', models.IntegerField(verbose_name='Рейтинг')),
                ('text', models.TextField(verbose_name='Текст')),
                ('is_publish', models.BooleanField(default=True, verbose_name='Опубликован')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='Дата обновления')),
                ('title', models.CharField(max_length=128, verbose_name='Заголовок')),
                ('desc', models.CharField(max_length=512, verbose_name='Описание')),
                ('text', models.TextField(verbose_name='Текст')),
                ('img', models.ImageField(upload_to='sales', verbose_name='Изображение')),
                ('is_publish', models.BooleanField(default=False, verbose_name='Опубликована')),
            ],
            options={
                'verbose_name': 'Акция',
                'verbose_name_plural': 'Акции',
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='Salon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='Дата обновления')),
                ('name', models.CharField(max_length=128, verbose_name='Наименование')),
                ('address', models.CharField(max_length=256, verbose_name='Адрес')),
                ('phone', apps.auth_app.fields.PhoneField(blank=True, max_length=20, null=True, verbose_name='Телефон')),
                ('desc', models.TextField(verbose_name='Описание')),
                ('is_publish', models.BooleanField(default=False, verbose_name='Опубликован')),
            ],
            options={
                'verbose_name': 'Салон',
                'verbose_name_plural': 'Салоны',
                'ordering': ['address'],
            },
        ),
        migrations.CreateModel(
            name='SalonImg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='Дата обновления')),
                ('img', models.ImageField(upload_to='salons', verbose_name='Изображение салона')),
                ('is_main', models.BooleanField(default=False, verbose_name='Главное фото')),
                ('is_publish', models.BooleanField(default=False, verbose_name='Опубликовано')),
            ],
            options={
                'verbose_name': 'Изображение салона',
                'verbose_name_plural': 'Изображения салона',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Specialist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='Дата обновления')),
                ('name', models.CharField(max_length=128, verbose_name='Имя')),
                ('photo', models.ImageField(upload_to='specialists', verbose_name='Фото')),
                ('position', models.CharField(max_length=128, verbose_name='Должность')),
                ('experience', models.CharField(max_length=128, verbose_name='Стаж работы')),
                ('title', models.CharField(blank=True, max_length=128, null=True, verbose_name='Заголовок описания')),
                ('text', models.TextField(verbose_name='Полное описание')),
                ('is_publish', models.BooleanField(default=False, verbose_name='Опубликовано')),
                ('salons', models.ManyToManyField(related_name='specialists', to='salon.salon', verbose_name='Салоны')),
            ],
            options={
                'verbose_name': 'Специалист',
                'verbose_name_plural': 'Специалисты',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='WorkImg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='Дата обновления')),
                ('name', models.CharField(blank=True, max_length=128, null=True, verbose_name='Наименование')),
                ('img', models.ImageField(upload_to='works', verbose_name='Выполненная работа')),
                ('is_publish', models.BooleanField(default=False, verbose_name='Опубликовано')),
                ('spec', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='work_imgs', to='salon.specialist', verbose_name='Сотрудник')),
            ],
            options={
                'verbose_name': 'Пример работы',
                'verbose_name_plural': 'Примеры работ',
                'ordering': ['-updated_at'],
            },
        ),
    ]
