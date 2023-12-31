# Generated by Django 4.2.6 on 2023-11-11 04:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_wiki_depth'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileRepository',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_type', models.SmallIntegerField(choices=[(1, 'Folder'), (2, 'File')], verbose_name='Upload Type')),
                ('name', models.CharField(help_text='File/Directory Name', max_length=128, verbose_name='File Name')),
                ('key', models.CharField(blank=True, max_length=128, null=True, verbose_name='s3 stored key')),
                ('file_size', models.IntegerField(blank=True, null=True, verbose_name='File Size')),
                ('file_path', models.CharField(blank=True, max_length=255, null=True, verbose_name='File Path')),
                ('update_datetime', models.DateTimeField(auto_now=True, verbose_name='Last Update Time')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child', to='web.filerepository', verbose_name='Parent')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.project', verbose_name='Project')),
                ('update_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.userinfo', verbose_name='Last Update User')),
            ],
        ),
    ]
