# Generated by Django 4.2.7 on 2024-01-21 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_user', models.CharField(max_length=200)),
                ('written_at', models.TimeField()),
                ('message', models.CharField(max_length=500)),
            ],
        ),
    ]
