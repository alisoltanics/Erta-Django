# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-04 10:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ertaapp', '0011_auto_20180204_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_code',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
