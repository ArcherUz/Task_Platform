# Generated by Django 4.2.6 on 2023-11-08 00:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_pricepolicy_project_transaction_projectuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wiki',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='Title')),
                ('content', models.TextField(verbose_name='Content')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='web.wiki', verbose_name='Parent')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.project', verbose_name='Project')),
            ],
        ),
    ]
