# Generated by Django 3.1.1 on 2021-02-06 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0005_auto_20210202_0231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empire',
            name='name',
            field=models.CharField(max_length=75),
        ),
    ]
