# Generated by Django 4.2.16 on 2024-11-04 23:39

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("custom_auth", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="emailverificationtoken",
            name="token",
            field=models.CharField(
                default=uuid.uuid4, editable=False, max_length=36, unique=True
            ),
        ),
    ]
