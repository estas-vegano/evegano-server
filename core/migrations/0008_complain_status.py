# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-20 17:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_complain_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='complain',
            name='status',
            field=models.CharField(choices=[('new', 'New'), ('postponed', 'Postponed'), ('rejected', 'Rejected'), ('done', 'Done')], default='new', max_length=16),
        ),
    ]
