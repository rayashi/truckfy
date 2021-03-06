# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-22 19:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('personas', '0003_auto_20170322_1623'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.IntegerField(default=5)),
                ('text', models.TextField(blank=True, default=None, max_length=600, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personas.Client')),
                ('truck', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personas.Truck')),
            ],
            options={
                'verbose_name_plural': 'Reviews',
            },
        ),
    ]
