# Generated by Django 4.2.16 on 2024-10-06 23:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("company_info", "0006_companyprofilemodel_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="CompanyProfileModel",
        ),
        migrations.AlterModelOptions(
            name="stockprice",
            options={"ordering": ["date"]},
        ),
        migrations.AlterModelOptions(
            name="stockvolume",
            options={"ordering": ["date"]},
        ),
        migrations.AddField(
            model_name="stockprice",
            name="moving_average_20",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="stockprice",
            name="moving_average_200",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="stockprice",
            name="moving_average_50",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="stockprice",
            name="ticker",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="stock_prices",
                to="company_info.companyprofile",
            ),
        ),
        migrations.AlterField(
            model_name="stockvolume",
            name="ticker",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="stock_volumes",
                to="company_info.companyprofile",
            ),
        ),
        migrations.AlterField(
            model_name="stockvolume",
            name="volume",
            field=models.BigIntegerField(),
        ),
        migrations.AlterUniqueTogether(
            name="stockprice",
            unique_together={("ticker", "date")},
        ),
        migrations.AlterUniqueTogether(
            name="stockvolume",
            unique_together={("ticker", "date")},
        ),
        migrations.AlterModelTable(
            name="stockprice",
            table="company_info_stockprice",
        ),
        migrations.AlterModelTable(
            name="stockvolume",
            table="company_info_stockvolume",
        ),
        migrations.RemoveField(
            model_name="stockprice",
            name="moving_average",
        ),
    ]
