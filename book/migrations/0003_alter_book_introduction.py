# Generated by Django 3.2.9 on 2023-06-12 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_auto_20230612_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='introduction',
            field=models.CharField(default='', max_length=50, verbose_name='时间'),
        ),
    ]
