# Generated by Django 2.0.3 on 2018-04-01 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allergies', '0002_auto_20180331_2334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='request_link',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
