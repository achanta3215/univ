# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0003_auto_20151109_1532'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='dept',
            new_name='dname',
        ),
    ]
