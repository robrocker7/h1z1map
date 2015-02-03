# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0002_player_last_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='last_updated',
            field=models.DateTimeField(db_index=True, null=True, blank=True),
            preserve_default=True,
        ),
    ]
