# Generated by Django 5.1.2 on 2024-10-15 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idapp', '0023_payslipdata_basic_salary_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payslipdata',
            name='dob',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='payslipdata',
            name='employment_date',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='payslipdata',
            name='retirement_date',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
