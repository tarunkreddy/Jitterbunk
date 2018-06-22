# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Bunk, UserProfile

admin.site.register(Bunk)
admin.site.register(UserProfile)

# Register your models here.
