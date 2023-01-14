# Generated by Django 4.1.2 on 2023-01-14 06:34

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('salon', '0001_initial'),
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
                ('title', models.CharField(blank=True, max_length=128, null=True, verbose_name='Заголовок описания')),
                ('text', models.TextField(verbose_name='Полное описание')),
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
    ]
