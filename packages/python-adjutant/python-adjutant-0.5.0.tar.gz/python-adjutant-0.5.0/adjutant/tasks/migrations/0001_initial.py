# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-06-10 02:09
from __future__ import unicode_literals

import adjutant.tasks.models
from django.db import migrations, models
import django.utils.timezone
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20190610_0209'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name='Task',
                    fields=[
                        ('uuid', models.CharField(default=adjutant.tasks.models.hex_uuid, max_length=32, primary_key=True, serialize=False)),
                        ('hash_key', models.CharField(db_index=True, max_length=64)),
                        ('ip_address', models.GenericIPAddressField()),
                        ('keystone_user', jsonfield.fields.JSONField(default={})),
                        ('project_id', models.CharField(db_index=True, max_length=64, null=True)),
                        ('approved_by', jsonfield.fields.JSONField(default={})),
                        ('task_type', models.CharField(db_index=True, max_length=100)),
                        ('action_notes', jsonfield.fields.JSONField(default={})),
                        ('cancelled', models.BooleanField(db_index=True, default=False)),
                        ('approved', models.BooleanField(db_index=True, default=False)),
                        ('completed', models.BooleanField(db_index=True, default=False)),
                        ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                        ('approved_on', models.DateTimeField(null=True)),
                        ('completed_on', models.DateTimeField(null=True)),
                    ],
                    options={
                        'indexes': [],
                    },
                ),
            ],
        ),
    ]
