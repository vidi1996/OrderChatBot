# Generated by Django 3.0.3 on 2020-02-10 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrderDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Choice', models.CharField(max_length=50)),
                ('Type', models.CharField(max_length=50)),
                ('Customize', models.CharField(max_length=50)),
                ('Quantity', models.IntegerField()),
                ('Address', models.CharField(max_length=50)),
            ],
        ),
    ]
