# Generated by Django 2.0.5 on 2018-06-16 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_auto_20180616_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='form',
            name='file',
            field=models.FileField(upload_to='documents/'),
        ),
    ]
