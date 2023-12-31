# Generated by Django 3.2.9 on 2023-06-12 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='price',
        ),
        migrations.RemoveField(
            model_name='book',
            name='url',
        ),
        migrations.AlterField(
            model_name='book',
            name='introduction',
            field=models.DateField(default='', verbose_name='时间'),
        ),
        migrations.AlterField(
            model_name='book',
            name='name',
            field=models.CharField(default='', max_length=50, verbose_name='电影名'),
        ),
        migrations.AlterField(
            model_name='book',
            name='publish',
            field=models.CharField(blank=True, default='', max_length=50, verbose_name='演员'),
        ),
    ]
