# Generated by Django 4.2.6 on 2023-11-17 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_filerepository'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filerepository',
            name='name',
            field=models.CharField(help_text='File/Directory Name', max_length=128, verbose_name='Folder/File Name'),
        ),
    ]
