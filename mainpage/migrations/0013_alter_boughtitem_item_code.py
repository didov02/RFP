# Generated by Django 4.2.7 on 2024-02-09 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0012_alter_boughtitem_item_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boughtitem',
            name='item_code',
            field=models.CharField(default='574B8B', max_length=10, unique=True),
        ),
    ]
