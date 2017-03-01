# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-01 18:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('personas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('text', models.TextField(blank=True, default=None, max_length=600, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('truck', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personas.Truck')),
            ],
            options={
                'verbose_name_plural': 'Pratos',
            },
        ),
    ]
