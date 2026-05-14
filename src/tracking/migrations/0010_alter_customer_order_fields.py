# Generated migration for fixing model conflicts with OrderExcelImportService
# Date: 2026-05-13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0009_alter_city_options_alter_city_name_alter_city_state_and_more'),
    ]

    operations = [
        # Customer alterations
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cnpj',
            field=models.CharField(max_length=14, unique=True, verbose_name='CNPJ'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tracking.city'),
        ),
        
        # Order alterations
        migrations.AlterField(
            model_name='order',
            name='nfe',
            field=models.CharField(max_length=20, unique=True, verbose_name='Número NFE'),
        ),
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tracking.customer', verbose_name='Cliente'),
        ),
        migrations.AlterField(
            model_name='order',
            name='carrier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tracking.carrier', verbose_name='Transportadora'),
        ),
    ]
