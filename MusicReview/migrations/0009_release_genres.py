# Generated by Django 4.2.11 on 2024-04-22 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MusicReview', '0008_alter_release_last_reviewed'),
    ]

    operations = [
        migrations.AddField(
            model_name='release',
            name='genres',
            field=models.CharField(default='Shoegaze, emo', max_length=1000),
            preserve_default=False,
        ),
    ]