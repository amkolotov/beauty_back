# Generated by Django 4.1.2 on 2023-01-29 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0009_mobileappsection_img_for_section_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='salon',
            name='short_desc',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Краткое описание'),
        ),
    ]
