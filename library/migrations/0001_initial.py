# Generated by Django 5.2 on 2025-04-10 13:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=255)),
                ('cover', models.CharField(choices=[('Hard Cover', 'Hard'), ('Soft Cover', 'Soft')], max_length=20)),
                ('inventory', models.PositiveIntegerField()),
                ('daily_fee', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('PAID', 'Paid')], default='PENDING', max_length=7)),
                ('type', models.CharField(choices=[('PAYMENT', 'Payment'), ('FINE', 'Fine')], max_length=7)),
                ('session_url', models.URLField(max_length=500)),
                ('session_id', models.CharField(max_length=255)),
                ('money_to_pay', models.DecimalField(decimal_places=2, max_digits=7)),
            ],
        ),
        migrations.CreateModel(
            name='Borrowing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrow_date', models.DateField(auto_now_add=True)),
                ('expected_return_date', models.DateField()),
                ('actual_return_date', models.DateField(blank=True, null=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.book')),
            ],
        ),
    ]
