# Generated by Django 5.0.6 on 2024-05-21 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_paper_views_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='paper',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
