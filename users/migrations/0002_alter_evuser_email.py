# Generated by Django 3.2.3 on 2021-05-21 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
