# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-10-07 08:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=2000, verbose_name='内容')),
                ('nickname', models.CharField(max_length=50, verbose_name='昵称')),
                ('website', models.URLField(verbose_name='网站')),
                ('email', models.EmailField(max_length=254, verbose_name='邮箱')),
                ('status', models.PositiveIntegerField(choices=[(1, '正常'), (2, '删除')], default=1, verbose_name='状态')),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Post', verbose_name='评论')),
            ],
            options={
                'verbose_name': '评论',
                'verbose_name_plural': '评论',
            },
        ),
    ]
