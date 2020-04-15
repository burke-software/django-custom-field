# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("custom_field", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customfield",
            name="field_choices",
            field=models.CharField(
                help_text=b"List the choices you want displayed, seperated by commas. This is only valid for Dropdown, Multiple, and Checkbox field types",
                max_length=2000,
                blank=True,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="customfield",
            name="is_required",
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="customfield",
            name="default_value",
            field=models.CharField(
                help_text=b"You may leave blank. For Boolean use True or False",
                max_length=5000,
                blank=True,
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="customfield",
            name="field_type",
            field=models.CharField(
                default=b"t",
                max_length=1,
                choices=[
                    (b"t", b"Text"),
                    (b"a", b"Large Text Field"),
                    (b"i", b"Integer"),
                    (b"f", b"Floating point decimal"),
                    (b"b", b"Boolean (Yes/No)"),
                    (b"m", b"Dropdown Choices"),
                    (b"d", b"Date"),
                ],
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="customfield",
            name="name",
            field=models.CharField(max_length=150),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="customfieldvalue",
            name="value",
            field=models.CharField(max_length=5000, null=True, blank=True),
            preserve_default=True,
        ),
    ]
