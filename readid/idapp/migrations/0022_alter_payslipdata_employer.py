# Generated by Django 5.1.2 on 2024-10-15 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idapp', '0021_employerdata_remove_payslipdata_basic_salary_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payslipdata',
            name='employer',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]