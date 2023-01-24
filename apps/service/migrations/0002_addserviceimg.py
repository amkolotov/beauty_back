# Generated by Django 4.1.2 on 2023-01-22 06:07

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddServiceImg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='Дата обновления')),
                ('img', models.ImageField(upload_to='services_types_site', verbose_name='Изображение услуги для сайта')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_imgs', to='service.servicecategory', verbose_name='Услуга')),
            ],
            options={
                'verbose_name': 'Изображение для сайта',
                'verbose_name_plural': 'Изображения для сайта',
                'ordering': ['service'],
            },
        ),
    ]