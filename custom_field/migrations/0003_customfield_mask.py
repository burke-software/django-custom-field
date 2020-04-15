# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("custom_field", "0002_auto_20150119_2032"),
    ]

    operations = [
        migrations.AddField(
            model_name="customfield",
            name="mask",
            field=models.CharField(
                help_text=b"You may leave blank. For user Jquery Mask, ex: '00/00/0000' for date.",
                max_length=5000,
                blank=True,
            ),
        ),
    ]
