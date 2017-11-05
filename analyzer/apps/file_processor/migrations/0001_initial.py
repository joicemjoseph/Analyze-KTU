# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-05 14:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=64)),
                ('code', models.CharField(max_length=64, unique=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=60)),
                ('docfile', models.FileField(upload_to='documents/%Y/%m/%d')),
                ('sha_sum', models.CharField(max_length=256, unique=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_supplementary_result', models.BooleanField(default=False)),
            ],
            options={
                'get_latest_by': 'updated_at',
            },
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=64)),
                ('is_full_time', models.BooleanField()),
                ('year', models.CharField(max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(default='2017-18', max_length=4)),
                ('grade', models.CharField(blank=True, max_length=4)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('course_id', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='file_processor.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=10, null=True)),
                ('number', models.PositiveSmallIntegerField(null=True, unique=True)),
                ('minimum_credit', models.PositiveSmallIntegerField(default=10, null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=40)),
                ('reg_no', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='score',
            name='student_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='file_processor.Student'),
        ),
        migrations.AddField(
            model_name='program',
            name='semester_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='file_processor.Semester'),
        ),
        migrations.AddField(
            model_name='course',
            name='program_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='file_processor.Program'),
        ),
        migrations.AddField(
            model_name='course',
            name='semester_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='file_processor.Semester'),
        ),
    ]