# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-22 18:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bunker', '0002_userprofile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='photo',
            field=models.ImageField(default=b'/profilePics/default-profile-picture.png', upload_to=b'profilePics/'),
        ),
    ]
