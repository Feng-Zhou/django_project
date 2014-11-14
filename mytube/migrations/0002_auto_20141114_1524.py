# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mytube', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='url',
        ),
        migrations.AddField(
            model_name='movie',
            name='video',
            field=embed_video.fields.EmbedVideoField(default=''),
            preserve_default=True,
        ),
    ]
