# Generated by Django 3.2.5 on 2021-08-18 16:27

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import pathlib


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('A', 'All'), ('B', 'LGBT'), ('M', 'Movie'), ('H', 'Hijab'), ('P', 'Popular'), ('R', 'Raw'), ('U', 'Unpopular')], default='R', max_length=1, unique=True)),
                ('full_name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'ordering': ['full_name'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('text', models.CharField(default='new', max_length=4, unique=True)),
                ('video_count', models.IntegerField(default=0)),
                ('category', models.ForeignKey(blank=True, default=7, on_delete=django.db.models.deletion.SET_DEFAULT, to='videos.category')),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_path', models.FilePathField(path=pathlib.PureWindowsPath('C:/Users/noyana/source/repos/djvideosroot'), unique=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('file_size', models.PositiveBigIntegerField(default=0)),
                ('duration', models.TimeField()),
                ('file_count', models.PositiveIntegerField(null=True)),
                ('is_movie', models.BooleanField(default=False)),
                ('width', models.IntegerField(default=840)),
                ('height', models.IntegerField(default=480)),
                ('frame_rate', models.FloatField(default=23.96)),
                ('category', models.ForeignKey(blank=True, default=7, on_delete=django.db.models.deletion.SET_DEFAULT, to='videos.category')),
                ('tags', models.ManyToManyField(blank=True, to='videos.Tag')),
            ],
        ),
        migrations.AddField(
            model_name='tag',
            name='videos',
            field=models.ManyToManyField(blank=True, to='videos.Video'),
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400, unique=True)),
                ('video_count', models.IntegerField(default=0)),
                ('category', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='videos.category')),
            ],
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('gender', models.CharField(choices=[('F', 'Female'), ('T', 'Trans'), ('M', 'Male'), ('B', 'Bi')], default='F', max_length=1)),
                ('video_count', models.IntegerField(default=0)),
                ('popular', models.BooleanField(default=False)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='videos.category')),
                ('videos', models.ManyToManyField(blank=True, to='videos.Video')),
            ],
            managers=[
                ('men', django.db.models.manager.Manager()),
            ],
        ),
    ]