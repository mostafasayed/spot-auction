# Generated by Django 5.1.1 on 2024-10-29 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0005_auction_winner'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
