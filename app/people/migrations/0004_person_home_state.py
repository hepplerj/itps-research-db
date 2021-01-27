# Generated by Django 3.1.1 on 2021-01-27 23:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0002_auto_20210127_2307'),
        ('people', '0003_auto_20210113_0014'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='home_state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='places.state'),
        ),
    ]
