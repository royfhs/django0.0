# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='appoint',
            fields=[
                ('appointID', models.IntegerField(serialize=False, primary_key=True)),
                ('Appointdate', models.CharField(max_length=10)),
                ('Appointtime', models.CharField(max_length=5)),
                ('Number', models.CharField(max_length=10)),
                ('State', models.CharField(default=b'N/D', max_length=8)),
                ('Urgent', models.CharField(default='\u65e0\u9644\u52a0\u4fe1\u606f', max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Datadate', models.CharField(max_length=10)),
                ('Datatime', models.CharField(max_length=5)),
                ('Datatitle', models.CharField(max_length=60)),
            ],
        ),
        migrations.AlterField(
            model_name='teacher',
            name='birth',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='name',
            field=models.CharField(max_length=20),
        ),
        migrations.AddField(
            model_name='event',
            name='t_id',
            field=models.ForeignKey(to='teacher.teacher'),
        ),
        migrations.AddField(
            model_name='appoint',
            name='t_id',
            field=models.ForeignKey(to='teacher.teacher'),
        ),
    ]
