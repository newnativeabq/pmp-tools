# Generated by Django 2.1.5 on 2019-01-19 18:56

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('flashcard', '0003_auto_20190118_0640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flashcard',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 19, 18, 56, 6, 457823, tzinfo=utc)),
        ),
    ]