# Generated by Django 4.2.16 on 2024-10-05 10:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "company_info",
            "0002_alter_companyprofile_average_trading_volume_10d_and_more",
        ),
    ]

    operations = [
        migrations.RenameField(
            model_name="companyprofile",
            old_name="dividend_rate",
            new_name="payout_ratio",
        ),
    ]
