# Generated by Django 5.1.1 on 2024-09-18 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pccapp', '0014_remove_product_printing_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='uom',
            field=models.CharField(choices=[('NO', "No's"), ('ROLL', 'Roll'), ('PCS', 'Pcs'), ('SQM', 'SqM')], default=1, max_length=10),
            preserve_default=False,
        ),
    ]
