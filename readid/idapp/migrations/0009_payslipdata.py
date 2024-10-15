# Generated by Django 5.0.6 on 2024-08-29 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idapp', '0008_logbookdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaySlipData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employer_name', models.CharField(blank=True, max_length=100, null=True)),
                ('payroll_number', models.CharField(blank=True, max_length=100, null=True)),
                ('employee_name', models.CharField(blank=True, max_length=100, null=True)),
                ('station', models.CharField(blank=True, max_length=100, null=True)),
                ('id_number', models.CharField(blank=True, max_length=100, null=True)),
                ('tax_pin', models.CharField(blank=True, max_length=100, null=True)),
                ('basic_salary', models.CharField(blank=True, max_length=100, null=True)),
                ('rental_house_allowance', models.CharField(blank=True, max_length=100, null=True)),
                ('hardship_allowance', models.CharField(blank=True, max_length=100, null=True)),
                ('commuter_allowance', models.CharField(blank=True, max_length=100, null=True)),
                ('total_earnings', models.CharField(blank=True, max_length=100, null=True)),
                ('total_deductions', models.CharField(blank=True, max_length=100, null=True)),
                ('nett_pay', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]