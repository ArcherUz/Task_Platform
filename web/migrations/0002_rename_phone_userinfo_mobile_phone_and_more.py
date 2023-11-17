# Generated by Django 4.2.6 on 2023-11-02 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userinfo',
            old_name='phone',
            new_name='mobile_phone',
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='password',
            field=models.CharField(max_length=64, verbose_name='Password'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='username',
            field=models.CharField(db_index=True, max_length=32, verbose_name='Username'),
        ),
    ]