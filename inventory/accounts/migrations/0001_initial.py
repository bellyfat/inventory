# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-18 00:44
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import inventory.common.model_mixins
import inventory.common.storage


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('regions', '0001_initial'),
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('public_id', models.CharField(blank=True, help_text='Public ID to identify a individual user.', max_length=30, unique=True, verbose_name='Public User ID')),
                ('_role', models.SmallIntegerField(choices=[(0, 'Default User'), (1, 'Administrator')], default=0, help_text='The role of the user.', verbose_name='Role')),
                ('picture', models.ImageField(blank=True, help_text='Photo of the individual.', null=True, storage=inventory.common.storage.InventoryFileStorage(), upload_to=inventory.common.storage.create_file_path, verbose_name='Picture')),
                ('send_email', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, help_text='Set to YES if this individual needs to be sent an email.', verbose_name='Send Email')),
                ('need_password', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, help_text='Set to YES if this individual needs to reset their password.', verbose_name='Need Password')),
                ('dob', models.DateField(blank=True, help_text='The date of your birth.', null=True, verbose_name='Date of Birth')),
                ('address_01', models.CharField(blank=True, help_text='Address line one.', max_length=50, null=True, verbose_name='Address 1')),
                ('address_02', models.CharField(blank=True, help_text='Address line two.', max_length=50, null=True, verbose_name='Address 2')),
                ('city', models.CharField(blank=True, help_text='The city this individual lives in.', max_length=30, null=True, verbose_name='City')),
                ('postal_code', models.CharField(blank=True, help_text='The zip code of residence.', max_length=15, null=True, verbose_name='Postal Code')),
                ('project_default', models.CharField(blank=True, help_text='The default project public_id.', max_length=30, null=True, verbose_name='Project Default')),
                ('country', models.ForeignKey(blank=True, help_text='The country of residence.', null=True, on_delete=django.db.models.deletion.CASCADE, to='regions.Country', verbose_name='Country')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('language', models.ForeignKey(blank=True, help_text='The language code.', null=True, on_delete=django.db.models.deletion.CASCADE, to='regions.Language', verbose_name='Language')),
                ('subdivision', models.ForeignKey(blank=True, help_text='The state of residence.', null=True, on_delete=django.db.models.deletion.CASCADE, to='regions.Subdivision', verbose_name='State/Province')),
                ('timezone', models.ForeignKey(blank=True, help_text='The timezone.', null=True, on_delete=django.db.models.deletion.CASCADE, to='regions.TimeZone', verbose_name='Timezone')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name_plural': 'Users',
                'ordering': ('last_name', 'username'),
                'verbose_name': 'User',
            },
            bases=(inventory.common.model_mixins.ValidateOnSaveMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(help_text='The date and time of creation.', verbose_name='Date Created')),
                ('updated', models.DateTimeField(help_text='The date and time last updated.', verbose_name='Last Updated')),
                ('public_id', models.CharField(blank=True, help_text='Public ID to identify an individual secure answer.', max_length=30, unique=True, verbose_name='Public Answer ID')),
                ('answer', models.CharField(help_text='An answer to an authentication question.', max_length=250, verbose_name='Answer')),
                ('creator', models.ForeignKey(editable=False, help_text='The user who created this record.', on_delete=django.db.models.deletion.CASCADE, related_name='accounts_answer_creator_related', to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
            ],
            options={
                'verbose_name_plural': 'Answers',
                'ordering': ('question__question',),
                'verbose_name': 'Answer',
            },
            bases=(inventory.common.model_mixins.ValidateOnSaveMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(help_text='The date and time of creation.', verbose_name='Date Created')),
                ('updated', models.DateTimeField(help_text='The date and time last updated.', verbose_name='Last Updated')),
                ('active', models.BooleanField(default=True, help_text='If checked the record is active.', verbose_name='Active')),
                ('public_id', models.CharField(blank=True, help_text='Public ID to identify an individual security question.', max_length=30, unique=True, verbose_name='Public Question ID')),
                ('question', models.CharField(help_text='A question for authentication.', max_length=100, verbose_name='Question')),
                ('creator', models.ForeignKey(editable=False, help_text='The user who created this record.', on_delete=django.db.models.deletion.CASCADE, related_name='accounts_question_creator_related', to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
                ('updater', models.ForeignKey(editable=False, help_text='The last user to update this record.', on_delete=django.db.models.deletion.CASCADE, related_name='accounts_question_updater_related', to=settings.AUTH_USER_MODEL, verbose_name='Updater')),
            ],
            options={
                'verbose_name_plural': 'Questions',
                'ordering': ('question',),
                'verbose_name': 'Question',
            },
            bases=(inventory.common.model_mixins.ValidateOnSaveMixin, models.Model),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(help_text='The question relative to this answer.', on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='accounts.Question', verbose_name='Question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='updater',
            field=models.ForeignKey(editable=False, help_text='The last user to update this record.', on_delete=django.db.models.deletion.CASCADE, related_name='accounts_answer_updater_related', to=settings.AUTH_USER_MODEL, verbose_name='Updater'),
        ),
        migrations.AddField(
            model_name='answer',
            name='user',
            field=models.ForeignKey(help_text='User to which this answer applies.', on_delete=django.db.models.deletion.CASCADE, related_name='answers', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
