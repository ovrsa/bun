# Generated by Django 4.2.16 on 2024-10-05 09:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CompanyProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("company_name", models.CharField(max_length=255)),
                ("ticker", models.CharField(max_length=10, unique=True)),
                ("exchange", models.CharField(max_length=50)),
                ("market_category", models.CharField(max_length=50)),
                ("industry", models.CharField(max_length=50)),
                ("sector", models.CharField(max_length=50)),
                ("address", models.CharField(max_length=255)),
                ("phone_number", models.CharField(max_length=50)),
                ("website", models.CharField(max_length=255)),
                ("founding_year", models.IntegerField()),
                ("employee_count", models.IntegerField()),
                ("outstanding_shares", models.IntegerField()),
                ("market_capitalization", models.FloatField()),
                ("average_trading_volume_10d", models.IntegerField()),
                ("dividend_rate", models.FloatField()),
                ("dividend_percentage", models.FloatField()),
                ("business_description", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="StockVolume",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                ("volume", models.IntegerField()),
                (
                    "ticker",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="company_info.companyprofile",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="StockPrice",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                ("close", models.FloatField()),
                ("high", models.FloatField()),
                ("low", models.FloatField()),
                ("moving_average", models.FloatField()),
                ("rsi", models.IntegerField()),
                (
                    "ticker",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="company_info.companyprofile",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CompanyFinancials",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("fiscal_year", models.IntegerField()),
                ("total_revenue", models.FloatField()),
                ("normalized_ebitda", models.FloatField()),
                ("stockholders_equity", models.FloatField()),
                ("free_cash_flow", models.FloatField()),
                ("capital_expenditures", models.FloatField()),
                ("total_assets", models.FloatField()),
                ("total_liabilities", models.FloatField()),
                ("gross_profit", models.FloatField()),
                ("net_income_loss", models.FloatField()),
                ("net_debt", models.FloatField()),
                ("enterprise_value", models.FloatField()),
                ("ebitda_margin", models.FloatField()),
                ("net_debt_to_ebitda", models.FloatField()),
                ("roa", models.FloatField()),
                ("roe", models.FloatField()),
                ("debt_to_equity", models.FloatField()),
                ("operating_margin", models.FloatField()),
                ("cash_from_operations", models.FloatField()),
                ("change_in_working_capital", models.FloatField()),
                (
                    "ticker",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="company_info.companyprofile",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BusinessSegment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("segment_name", models.CharField(max_length=50)),
                ("description", models.TextField()),
                (
                    "ticker",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="business_segments",
                        to="company_info.companyprofile",
                    ),
                ),
            ],
        ),
    ]
