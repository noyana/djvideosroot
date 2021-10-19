# Generated by Django 3.2.5 on 2021-08-24 20:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0005_auto_20210824_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='category',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.SET_DEFAULT, to='videos.category'),
        ),
        migrations.AlterField(
            model_name='video',
            name='file_date',
            field=models.DateTimeField(),
        ),
    ]