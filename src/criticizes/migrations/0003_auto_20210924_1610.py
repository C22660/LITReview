# Generated by Django 3.1.6 on 2021-09-24 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('criticizes', '0002_auto_20210924_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='ticket_images'),
        ),
    ]
