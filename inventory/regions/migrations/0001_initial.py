# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-18 00:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import inventory.common.model_mixins


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, help_text='If checked the record is active.', verbose_name='Active')),
                ('country', models.CharField(help_text='The country name.', max_length=100, verbose_name='Country')),
                ('code', models.CharField(db_index=True, help_text='The two character country code.', max_length=2, unique=True, verbose_name='Code')),
            ],
            options={
                'verbose_name_plural': 'Countries',
                'ordering': ('country',),
                'verbose_name': 'Country',
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, help_text='If checked the record is active.', verbose_name='Active')),
                ('currency', models.CharField(help_text='Name of the currency.', max_length=50, verbose_name='Corrency')),
                ('alphabetic_code', models.CharField(help_text='3 digit alphabetic code for the currency.', max_length=3, verbose_name='Alphabetic Code')),
                ('numeric_code', models.PositiveSmallIntegerField(help_text='3 digit numeric code.', verbose_name='Numeric Code')),
                ('minor_unit', models.PositiveSmallIntegerField(help_text='Number of digits after the decimal separator.', verbose_name='Minor Unit')),
                ('symbol', models.CharField(blank=True, help_text='The symbol representing this currency.', max_length=6, null=True, verbose_name='Symbol')),
                ('country', models.ForeignKey(db_index=False, help_text='Country or region name.', on_delete=django.db.models.deletion.CASCADE, to='regions.Country', verbose_name='Country')),
            ],
            options={
                'verbose_name_plural': 'Currencies',
                'ordering': ('country__country', 'currency'),
                'verbose_name': 'Currency',
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, help_text='If checked the record is active.', verbose_name='Active')),
                ('locale', models.CharField(blank=True, help_text='The language and country codes.', max_length=5, unique=True, verbose_name='Locale')),
                ('code', models.CharField(help_text='The two character language code.', max_length=2, verbose_name='Language Code')),
                ('country', models.ForeignKey(help_text='The country.', on_delete=django.db.models.deletion.CASCADE, related_name='languages', to='regions.Country', verbose_name='Country')),
            ],
            options={
                'verbose_name_plural': 'Languages',
                'ordering': ('locale',),
                'verbose_name': 'Language',
            },
            bases=(inventory.common.model_mixins.ValidateOnSaveMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Subdivision',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, help_text='If checked the record is active.', verbose_name='Active')),
                ('subdivision_name', models.CharField(help_text='The subdivision of the country.', max_length=130, verbose_name='State')),
                ('code', models.CharField(help_text='The subdivision code.', max_length=10, verbose_name='State Code')),
                ('country', models.ForeignKey(db_index=False, help_text='The country.', on_delete=django.db.models.deletion.CASCADE, related_name='subdivisions', to='regions.Country', verbose_name='Country')),
            ],
            options={
                'verbose_name_plural': 'Subdivisions',
                'ordering': ('country', 'subdivision_name'),
                'verbose_name': 'Subdivision',
            },
        ),
        migrations.CreateModel(
            name='TimeZone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, help_text='If checked the record is active.', verbose_name='Active')),
                ('zone', models.CharField(help_text='The timezone (zoneinfo).', max_length=40, verbose_name='Timezone')),
                ('coordinates', models.CharField(help_text='Latitude & Longitude.', max_length=20, verbose_name='Coordinates')),
                ('desc', models.TextField(blank=True, help_text='Zone description.', null=True, verbose_name='Description')),
                ('country', models.ForeignKey(db_index=False, help_text='The country.', on_delete=django.db.models.deletion.CASCADE, related_name='timezones', to='regions.Country', verbose_name='Country')),
            ],
            options={
                'verbose_name_plural': 'Time Zones',
                'ordering': ('zone',),
                'verbose_name': 'Time Zone',
            },
        ),
        migrations.AlterUniqueTogether(
            name='timezone',
            unique_together=set([('country', 'zone')]),
        ),
        migrations.AlterUniqueTogether(
            name='subdivision',
            unique_together=set([('country', 'code')]),
        ),
        migrations.AlterUniqueTogether(
            name='currency',
            unique_together=set([('country', 'alphabetic_code')]),
        ),
    ]
