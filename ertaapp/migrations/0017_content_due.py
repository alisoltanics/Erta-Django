# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-06 14:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ertaapp', '0016_auto_20180205_1201'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='due',
            field=models.DateField(blank=True, default=django.utils.timezone.now),
        ),
    ]