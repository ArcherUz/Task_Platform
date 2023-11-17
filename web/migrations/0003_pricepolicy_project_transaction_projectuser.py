# Generated by Django 4.2.6 on 2023-11-03 07:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_rename_phone_userinfo_mobile_phone_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PricePolicy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.SmallIntegerField(choices=[(1, 'Free'), (2, 'VIP'), (3, 'SVIP')], default=2, verbose_name='Price Policy')),
                ('title', models.CharField(max_length=32, verbose_name='Title')),
                ('price', models.PositiveIntegerField(verbose_name='Price')),
                ('project_num', models.PositiveIntegerField(verbose_name='Project Number')),
                ('project_member', models.PositiveIntegerField(verbose_name='Project Member')),
                ('project_space', models.PositiveIntegerField(verbose_name='Single Project Size')),
                ('per_file_size', models.PositiveIntegerField(verbose_name='Single File Size')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Create Time')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='Project Name')),
                ('color', models.SmallIntegerField(choices=[(1, '#56b8eb'), (2, '#f28033'), (3, '#ebc656'), (4, '#a2d148'), (5, '#20bfa4'), (6, '#7461c2'), (7, '#20bfa3')], default=1, verbose_name='Color')),
                ('desc', models.CharField(blank=True, max_length=128, null=True, verbose_name='Description')),
                ('use_space', models.IntegerField(default=0, verbose_name='Used size')),
                ('star', models.BooleanField(default=False, verbose_name='Star')),
                ('join_count', models.SmallIntegerField(default=1, verbose_name='Join Count')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Create Time')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.userinfo', verbose_name='Creator')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.SmallIntegerField(choices=[(1, 'Not Paid'), (2, 'Paid')], verbose_name='Status')),
                ('order', models.CharField(max_length=64, unique=True, verbose_name='Order')),
                ('count', models.IntegerField(help_text='0 for unlimited time', verbose_name='Count (Year)')),
                ('price', models.IntegerField(verbose_name='Price')),
                ('start_datetime', models.DateTimeField(blank=True, null=True, verbose_name='Start Time')),
                ('end_datetime', models.DateTimeField(blank=True, null=True, verbose_name='End Time')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Create Time')),
                ('price_policy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.pricepolicy', verbose_name='Price Policy')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.userinfo', verbose_name='User')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('star', models.BooleanField(default=False, verbose_name='Star')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Create Time')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.project', verbose_name='Project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.userinfo', verbose_name='User')),
            ],
        ),
    ]
