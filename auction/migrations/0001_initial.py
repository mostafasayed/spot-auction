# Generated by Django 5.1.1 on 2024-09-25 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.URLField(blank=True, max_length=500, null=True)),
                ('date_type', models.CharField(max_length=100)),
                ('quantity', models.IntegerField()),
                ('avg_piece_weight', models.DecimalField(decimal_places=2, max_digits=5)),
                ('category', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
