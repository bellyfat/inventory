# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-10 17:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inventorytype',
            options={'ordering': ('name',), 'verbose_name': 'InventoryType', 'verbose_name_plural': 'InventoryTypes'},
        ),
    ]