# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-18 00:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import inventory.common.model_mixins


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(help_text='The date and time of creation.', verbose_name='Date Created')),
                ('updated', models.DateTimeField(help_text='The date and time last updated.', verbose_name='Last Updated')),
                ('public_id', models.CharField(blank=True, help_text='Public ID to identify a individual category.', max_length=30, unique=True, verbose_name='Public Category ID')),
                ('name', models.CharField(help_text='The name of this category.', max_length=250, verbose_name='Name')),
                ('path', models.CharField(editable=False, help_text='The full hierarchical path of this category.', max_length=1000, verbose_name='Full Path')),
                ('level', models.SmallIntegerField(editable=False, help_text='The location in the hierarchy of this category.', verbose_name='Level')),
                ('creator', models.ForeignKey(editable=False, help_text='The user who created this record.', on_delete=django.db.models.deletion.CASCADE, related_name='categories_category_creator_related', to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
                ('parent', models.ForeignKey(blank=True, default=None, help_text='The parent to this category if any.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='categories.Category', verbose_name='Parent')),
                ('project', models.ForeignKey(db_index=False, help_text='The project that owns this record.', on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='projects.Project', verbose_name='Project')),
                ('updater', models.ForeignKey(editable=False, help_text='The last user to update this record.', on_delete=django.db.models.deletion.CASCADE, related_name='categories_category_updater_related', to=settings.AUTH_USER_MODEL, verbose_name='Updater')),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'ordering': ('path',),
                'verbose_name': 'Category',
            },
            bases=(inventory.common.model_mixins.ValidateOnSaveMixin, models.Model),
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together=set([('project', 'parent', 'name')]),
        ),
    ]
