# Generated by Django 5.0.6 on 2024-09-02 06:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('idapp', '0012_loanapplicationdata'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loanapplicationdata',
            name='loan_amount',
        ),
        migrations.RemoveField(
            model_name='loanapplicationdata',
            name='loan_tenure',
        ),
    ]
