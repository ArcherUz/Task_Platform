# Generated by Django 4.2.6 on 2023-11-08 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_wiki'),
    ]

    operations = [
        migrations.AddField(
            model_name='wiki',
            name='depth',
            field=models.IntegerField(default=1, verbose_name='Depth'),
        ),
    ]