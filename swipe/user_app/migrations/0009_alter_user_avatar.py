# Generated by Django 3.2.19 on 2023-05-31 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0008_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(upload_to='img/avatar/', verbose_name='Аватар'),
        ),
    ]
