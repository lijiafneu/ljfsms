# Generated by Django 2.1.4 on 2018-12-15 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='qq',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
