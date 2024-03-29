# Generated by Django 5.0.2 on 2024-02-26 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commodity', models.CharField(max_length=255)),
                ('market', models.CharField(max_length=255)),
                ('district', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('min_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('max_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('model_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('arrival_date', models.DateField()),
            ],
            options={
                'unique_together': {('commodity', 'market', 'district', 'arrival_date')},
            },
        ),
    ]
