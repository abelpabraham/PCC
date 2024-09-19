# Generated by Django 5.1.1 on 2024-09-14 17:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pccapp', '0007_delete_stock'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaperSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('width', models.DecimalField(decimal_places=2, max_digits=5)),
                ('height', models.DecimalField(decimal_places=2, max_digits=5)),
                ('cost_adjustment', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Substrate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('base_cost_per_unit', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='SubstrateSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('width', models.DecimalField(decimal_places=2, max_digits=5)),
                ('height', models.DecimalField(decimal_places=2, max_digits=5)),
                ('cost_adjustment', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='SubstrateThickness',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thickness_value', models.DecimalField(decimal_places=2, max_digits=5)),
                ('cost_adjustment', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='PaperConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paper_thickness', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pccapp.paperthickness')),
                ('paper_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pccapp.papertype')),
                ('paper_size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pccapp.papersize')),
            ],
        ),
        migrations.CreateModel(
            name='SubstrateConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('substrate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pccapp.substrate')),
                ('substrate_size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pccapp.substratesize')),
                ('substrate_thickness', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pccapp.substratethickness')),
            ],
        ),
    ]
