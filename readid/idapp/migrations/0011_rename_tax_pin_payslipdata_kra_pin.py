# Generated by Django 5.0.6 on 2024-08-30 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('idapp', '0010_rename_nett_pay_payslipdata_location_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payslipdata',
            old_name='tax_pin',
            new_name='kra_pin',
        ),
    ]