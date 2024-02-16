# Generated by Django 4.2.7 on 2024-02-15 19:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainpage', '0023_remove_reservation_date_remove_reservation_hour_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='reservation_participants', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='boughtitem',
            name='item_code',
            field=models.CharField(default='7D892C', max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='reservation_code',
            field=models.CharField(default='24E62A', max_length=10, unique=True),
        ),
    ]
