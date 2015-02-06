# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0003_auto_20150202_0409'),
    ]

    operations = [
        migrations.CreateModel(
            name='Move',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lat', models.FloatField(null=True, blank=True)),
                ('lng', models.FloatField(null=True, blank=True)),
                ('heading', models.FloatField(null=True, blank=True)),
                ('life', models.IntegerField(db_index=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='player',
            name='heading',
        ),
        migrations.RemoveField(
            model_name='player',
            name='lat',
        ),
        migrations.RemoveField(
            model_name='player',
            name='lng',
        ),
        migrations.AddField(
            model_name='player',
            name='current_life',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 6, 3, 59, 20, 812044, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='moves',
            field=models.ManyToManyField(to='players.Move'),
            preserve_default=True,
        ),
    ]
