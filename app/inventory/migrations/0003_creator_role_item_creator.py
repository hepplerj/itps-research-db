# Generated by Django 3.1.1 on 2020-09-29 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0001_initial'),
        ('organizations', '0001_initial'),
        ('inventory', '0002_auto_20200929_1442'),
    ]

    operations = [
        migrations.CreateModel(
            name='Creator_Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('notes', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item_Creator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField(blank=True, null=True)),
                ('item', models.ManyToManyField(to='inventory.Item')),
                ('organization', models.ManyToManyField(blank=True, to='organizations.Organization')),
                ('person', models.ManyToManyField(blank=True, to='people.Person')),
                ('role', models.ManyToManyField(to='inventory.Creator_Role')),
            ],
        ),
    ]
