# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-05 08:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ertaapp', '0014_auto_20180205_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='picture',
            field=models.ImageField(blank=True, default='media/course_pics/default_course.png', upload_to='course_pics'),
        ),
    ]
