# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2018-01-07 18:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0034_auto_20180107_1808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='status',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
    ]