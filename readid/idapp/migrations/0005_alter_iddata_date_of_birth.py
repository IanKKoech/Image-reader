# Generated by Django 5.0.6 on 2024-05-30 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idapp', '0004_alter_iddata_date_of_birth_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iddata',
            name='date_of_birth',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
