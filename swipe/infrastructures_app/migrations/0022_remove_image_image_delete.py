# Generated by Django 3.2.19 on 2023-06-16 11:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('infrastructures_app', '0021_image_hash'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='image_delete',
        ),
    ]
