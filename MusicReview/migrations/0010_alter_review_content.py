# Generated by Django 4.2.11 on 2024-04-22 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MusicReview', '0009_release_genres'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='content',
            field=models.TextField(blank=True),
        ),
    ]
