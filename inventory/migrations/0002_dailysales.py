# Generated by Django 5.0.1 on 2024-06-18 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailySales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
            ],
        ),
    ]
