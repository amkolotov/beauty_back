# Generated by Django 4.1.2 on 2023-03-31 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0019_ceo_alter_appreasons_img_alter_appreasons_title_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='salon',
            name='slug',
            field=models.SlugField(blank=True, help_text='Cоздается автоматически', max_length=255, null=True, unique=True, verbose_name='Слаг'),
        ),
    ]
