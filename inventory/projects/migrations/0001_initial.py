# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-18 00:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import inventory.common.model_mixins
import inventory.common.storage


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(help_text='The date and time of creation.', verbose_name='Date Created')),
                ('updated', models.DateTimeField(help_text='The date and time last updated.', verbose_name='Last Updated')),
                ('public_id', models.CharField(blank=True, help_text='Public ID to identify an individual inventory type.', max_length=30, unique=True, verbose_name='Public Inventory Type ID')),
                ('name', models.CharField(help_text='The name of the inventory type.', max_length=250, verbose_name='Inventory Type')),
                ('description', models.CharField(blank=True, help_text='Define what the codes derived from this format are used for.', max_length=250, null=True, verbose_name='Description')),
                ('creator', models.ForeignKey(editable=False, help_text='The user who created this record.', on_delete=django.db.models.deletion.CASCADE, related_name='projects_inventorytype_creator_related', to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
                ('updater', models.ForeignKey(editable=False, help_text='The last user to update this record.', on_delete=django.db.models.deletion.CASCADE, related_name='projects_inventorytype_updater_related', to=settings.AUTH_USER_MODEL, verbose_name='Updater')),
            ],
            options={
                'verbose_name_plural': 'InventoryTypes',
                'verbose_name': 'InventoryType',
            },
            bases=(inventory.common.model_mixins.ValidateOnSaveMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.SmallIntegerField(choices=[(0, 'Project User'), (1, 'Project Owner'), (2, 'Project Manager')], default=0, help_text='The role of the user.', verbose_name='Role')),
            ],
            options={
                'verbose_name_plural': 'Memberships',
                'verbose_name': 'Membership',
            },
            bases=(inventory.common.model_mixins.ValidateOnSaveMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(help_text='The date and time of creation.', verbose_name='Date Created')),
                ('updated', models.DateTimeField(help_text='The date and time last updated.', verbose_name='Last Updated')),
                ('active', models.BooleanField(default=True, help_text='If checked the record is active.', verbose_name='Active')),
                ('public_id', models.CharField(blank=True, help_text='Public ID to identify an individual project.', max_length=30, unique=True, verbose_name='Public Project ID')),
                ('name', models.CharField(help_text='The name of the project.', max_length=250, verbose_name='Project Name')),
                ('image', models.ImageField(blank=True, help_text='Upload project logo image.', null=True, storage=inventory.common.storage.InventoryFileStorage(), upload_to=inventory.common.storage.create_file_path, verbose_name='Project Image')),
                ('public', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=True, help_text='Set to YES if this project is public else set to NO.', verbose_name='Public')),
                ('creator', models.ForeignKey(editable=False, help_text='The user who created this record.', on_delete=django.db.models.deletion.CASCADE, related_name='projects_project_creator_related', to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
                ('inventory_type', models.ForeignKey(help_text='The inventory type.', on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='projects.InventoryType', verbose_name='Inventory Type')),
                ('members', models.ManyToManyField(blank=True, help_text='The members of this project.', related_name='projects', through='projects.Membership', to=settings.AUTH_USER_MODEL, verbose_name='Project Members')),
                ('updater', models.ForeignKey(editable=False, help_text='The last user to update this record.', on_delete=django.db.models.deletion.CASCADE, related_name='projects_project_updater_related', to=settings.AUTH_USER_MODEL, verbose_name='Updater')),
            ],
            options={
                'verbose_name_plural': 'Projects',
                'ordering': ('name',),
                'verbose_name': 'Project',
            },
            bases=(inventory.common.model_mixins.ValidateOnSaveMixin, models.Model),
        ),
        migrations.AddField(
            model_name='membership',
            name='project',
            field=models.ForeignKey(help_text='The project.', on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to='projects.Project', verbose_name='Project'),
        ),
        migrations.AddField(
            model_name='membership',
            name='user',
            field=models.ForeignKey(help_text='The user.', on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
