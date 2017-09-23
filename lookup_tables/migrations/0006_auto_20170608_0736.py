# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-06-08 17:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lookup_tables', '0005_delete_bait'),
    ]

    operations = [
        migrations.AlterField(
            model_name='speciesdef',
            name='size_class',
            field=models.CharField(choices=[(b'Small', b'Small'), (b'Medium', b'Medium'), (b'Large', b'Large'), (b'Rat', b'Rat')], max_length=20),
        ),
        migrations.AlterField(
            model_name='speciesdef',
            name='species_code',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
