# Generated by Django 4.1.2 on 2023-02-01 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='expo_token',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Push токен'),
        ),
    ]
