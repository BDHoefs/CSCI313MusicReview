# Generated by Django 4.2.11 on 2024-04-22 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MusicReview', '0003_release_release_type_alter_song_length'),
    ]

    operations = [
        migrations.AlterField(
            model_name='release',
            name='reviews',
            field=models.ManyToManyField(null=True, to='MusicReview.review'),
        ),
    ]
