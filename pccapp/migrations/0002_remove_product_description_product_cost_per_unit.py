# Generated by Django 5.1.1 on 2024-09-13 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pccapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='description',
        ),
        migrations.AddField(
            model_name='product',
            name='cost_per_unit',
            field=models.DecimalField(decimal_places=2, default=20.0, max_digits=10),
            preserve_default=False,
        ),
    ]
