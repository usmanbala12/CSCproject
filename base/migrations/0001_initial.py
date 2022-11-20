# Generated by Django 4.1.3 on 2022-11-19 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('capacity', models.IntegerField()),
                ('name', models.CharField(max_length=15)),
                ('model_name', models.CharField(max_length=100)),
                ('number', models.CharField(max_length=10)),
            ],
        ),
    ]
