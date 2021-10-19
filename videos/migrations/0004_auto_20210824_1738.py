# Generated by Django 3.2.5 on 2021-08-24 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0003_auto_20210820_1807'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='artist',
            options={'ordering': ['-video_count', 'name']},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['full_name'], 'verbose_name_plural': 'categories'},
        ),
        migrations.AlterModelOptions(
            name='video',
            options={'ordering': ['-file_count', 'name']},
        ),
        migrations.AlterModelManagers(
            name='artist',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='artist',
            name='popular',
        ),
        migrations.AddIndex(
            model_name='video',
            index=models.Index(fields=['name'], name='videos_vide_name_c70b89_idx'),
        ),
        migrations.AddIndex(
            model_name='video',
            index=models.Index(fields=['is_movie', 'name'], name='videos_vide_is_movi_b7795b_idx'),
        ),
        migrations.AddIndex(
            model_name='video',
            index=models.Index(fields=['file_size'], name='videos_vide_file_si_b449c9_idx'),
        ),
    ]
