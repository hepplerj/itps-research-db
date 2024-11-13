# Generated by Django 5.1.3 on 2024-11-13 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("people", "0006_alter_person_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="person",
            name="display_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="person",
            name="name",
            field=models.CharField(max_length=255),
        ),
    ]
