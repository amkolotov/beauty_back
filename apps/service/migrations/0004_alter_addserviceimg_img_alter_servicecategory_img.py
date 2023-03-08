# Generated by Django 4.1.2 on 2023-03-08 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0003_alter_addserviceimg_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addserviceimg',
            name='img',
            field=models.ImageField(help_text='Рекомендуемый размер 370Х310px', upload_to='services_types_site', verbose_name='Изображение услуги для сайта'),
        ),
        migrations.AlterField(
            model_name='servicecategory',
            name='img',
            field=models.ImageField(help_text='Рекомендуемый размер 370Х310px', upload_to='service_types', verbose_name='Изображение'),
        ),
    ]