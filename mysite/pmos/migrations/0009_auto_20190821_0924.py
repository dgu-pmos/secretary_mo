# Generated by Django 2.2.3 on 2019-08-21 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pmos', '0008_auto_20190821_0920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memocond',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
