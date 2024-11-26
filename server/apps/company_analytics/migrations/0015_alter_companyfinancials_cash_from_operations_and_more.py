# Generated by Django 4.2.16 on 2024-10-28 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("company_info", "0014_companyfinancials_updated_at_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="companyfinancials",
            name="cash_from_operations",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="companyfinancials",
            name="change_in_working_capital",
            field=models.FloatField(blank=True, null=True),
        ),
    ]