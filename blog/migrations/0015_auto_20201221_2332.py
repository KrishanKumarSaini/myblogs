# Generated by Django 2.2 on 2020-12-21 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_auto_20201221_2331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='thumbnail',
            field=models.ImageField(default='/avatar-2.jpg', upload_to=''),
        ),
    ]
