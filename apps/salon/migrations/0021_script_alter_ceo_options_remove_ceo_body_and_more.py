# Generated by Django 4.1.2 on 2023-04-09 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0020_salon_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Script',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Дата обновления')),
                ('name', models.CharField(max_length=128, verbose_name='Наименование')),
                ('script', models.TextField(blank=True, help_text='Добавить без тега script', null=True, verbose_name='Скрипт')),
            ],
            options={
                'verbose_name': 'Скрипт',
                'verbose_name_plural': 'Скрипты',
            },
        ),
        migrations.AlterModelOptions(
            name='ceo',
            options={'verbose_name': 'CEO', 'verbose_name_plural': 'CEO'},
        ),
        migrations.RemoveField(
            model_name='ceo',
            name='body',
        ),
        migrations.AlterField(
            model_name='ceo',
            name='head',
            field=models.TextField(blank=True, help_text='Добавить общим html', null=True, verbose_name='Кастомный Head'),
        ),
        migrations.AddField(
            model_name='ceo',
            name='body_scripts',
            field=models.ManyToManyField(blank=True, null=True, related_name='body_scripts', to='salon.script'),
        ),
        migrations.AddField(
            model_name='ceo',
            name='head_scripts',
            field=models.ManyToManyField(blank=True, null=True, related_name='head_scripts', to='salon.script'),
        ),
    ]
