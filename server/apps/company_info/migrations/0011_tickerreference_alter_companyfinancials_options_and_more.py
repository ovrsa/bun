# Generated by Django 4.2.16 on 2024-10-14 04:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("company_info", "0010_stockprice_volume_delete_stockvolume"),
    ]

    operations = [
        migrations.CreateModel(
            name="TickerReference",
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
                ("ticker", models.CharField(max_length=10, unique=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name="companyfinancials",
            options={"ordering": ["fiscal_year"]},
        ),
        migrations.AlterModelTable(
            name="companyfinancials",
            table="company_financials",
        ),
        migrations.AlterModelTable(
            name="companyprofile",
            table="company_profile",
        ),
        migrations.AlterModelTable(
            name="stockprice",
            table="stock_price",
        ),
        migrations.AlterField(
            model_name="companyfinancials",
            name="ticker",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="company_financials",
                to="company_info.tickerreference",
            ),
        ),
        migrations.AlterField(
            model_name="companyprofile",
            name="ticker",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="company_profile",
                to="company_info.tickerreference",
            ),
        ),
        migrations.AlterField(
            model_name="stockprice",
            name="ticker",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="stock_prices",
                to="company_info.tickerreference",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="companyfinancials",
            unique_together={("ticker", "fiscal_year")},
        ),
    ]
