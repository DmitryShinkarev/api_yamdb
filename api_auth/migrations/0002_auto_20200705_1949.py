# Generated by Django 3.0.5 on 2020-07-05 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_auth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auth',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email'),
        ),
    ]
