# Generated by Django 3.2.3 on 2021-05-29 10:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aws', '0002_alter_awsdocument_document'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='evuser',
            name='profile_image',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='aws.awsdocument'),
        ),
    ]
