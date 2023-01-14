# Generated by Django 4.1.2 on 2023-01-14 06:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='Дата обновления')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars', verbose_name='Аватар')),
            ],
            options={
                'verbose_name': 'Профиль пользователя',
                'verbose_name_plural': 'Профили пользователей',
                'db_table': 'profile',
            },
        ),
    ]
