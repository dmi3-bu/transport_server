# Generated by Django 2.2.3 on 2019-07-13 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20190713_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='passport',
            field=models.IntegerField(),
        ),
    ]
