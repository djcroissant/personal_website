# Generated by Django 2.0.5 on 2018-06-13 22:21

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('crmblog', '0002_auto_20180609_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=tinymce.models.HTMLField(blank=True),
        ),
    ]