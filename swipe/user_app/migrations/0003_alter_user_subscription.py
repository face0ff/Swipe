# Generated by Django 3.2.19 on 2023-05-27 22:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0002_alter_subscription_paid_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='subscription',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='user_app.subscription'),
        ),
    ]
