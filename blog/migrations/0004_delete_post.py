# Generated by Django 2.2 on 2020-12-17 16:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_author'),
    ]

    operations = [
        migrations.DeleteModel(
            name='post',
        ),
    ]