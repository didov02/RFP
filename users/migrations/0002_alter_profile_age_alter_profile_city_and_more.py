# Generated by Django 4.2.7 on 2024-02-07 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='age',
            field=models.IntegerField(default=15),
        ),
        migrations.AlterField(
            model_name='profile',
            name='city',
            field=models.CharField(default='Unknown', max_length=200),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='profile_pictures/profilepic.jpg', upload_to='profile_pictures'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='position',
            field=models.CharField(default='Unknown', max_length=200),
        ),
    ]