# Generated by Django 5.0.6 on 2024-09-02 12:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idapp', '0019_delete_loanapplicationdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoanApplicationData',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('loan_amount', models.CharField(blank=True, default='0.00', max_length=100, null=True)),
                ('loan_tenure', models.CharField(blank=True, default='N/A', max_length=100, null=True)),
                ('id_data', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='idapp.iddata')),
                ('payslip_data', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='idapp.payslipdata')),
            ],
        ),
    ]
