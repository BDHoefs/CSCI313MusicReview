# Generated by Django 4.2.11 on 2024-04-22 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MusicReview', '0004_alter_release_reviews'),
    ]

    operations = [
        migrations.AlterField(
            model_name='release',
            name='last_reviewed',
            field=models.DateTimeField(null=True),
        ),
    ]
