# Generated by Django 5.2 on 2025-04-13 13:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_alter_borrowing_book_alter_borrowing_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover',
            field=models.CharField(choices=[('HARD', 'Hard Cover'), ('SOFT', 'Soft Cover')], max_length=20),
        ),
        migrations.AlterField(
            model_name='payment',
            name='borrowing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='library.borrowing'),
        ),
    ]
