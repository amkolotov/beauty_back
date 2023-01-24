# Generated by Django 4.1.2 on 2023-01-22 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0004_mobileappsection_alter_faq_options_store'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mobileappsection',
            options={'ordering': ['-created_at'], 'verbose_name': 'Секция мобильного приложения', 'verbose_name_plural': 'Секция мобильного приложения'},
        ),
        migrations.AlterField(
            model_name='messengertype',
            name='name',
            field=models.CharField(max_length=28, verbose_name='Наименование'),
        ),
    ]