# Generated by Django 2.1.5 on 2019-01-20 05:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('flashcard', '0004_auto_20190119_1156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flashcard',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 20, 5, 5, 12, 728181, tzinfo=utc)),
        ),
    ]
