# Generated by Django 5.2.4 on 2025-07-18 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
