# Generated by Django 4.2.7 on 2024-02-15 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0022_reservation_date_reservation_hour_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='date',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='hour',
        ),
        migrations.AddField(
            model_name='reservation',
            name='datetime',
            field=models.DateTimeField(default='2024-01-01T08:00'),
        ),
        migrations.AlterField(
            model_name='boughtitem',
            name='item_code',
            field=models.CharField(default='A1FED8', max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='reservation_code',
            field=models.CharField(default='66F0CA', max_length=10, unique=True),
        ),
    ]
