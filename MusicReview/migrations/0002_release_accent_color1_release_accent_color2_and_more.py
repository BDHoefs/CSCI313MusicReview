# Generated by Django 4.2.11 on 2024-04-22 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MusicReview', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='release',
            name='accent_color1',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='release',
            name='accent_color2',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='release',
            name='accent_color3',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='release',
            name='accent_color4',
            field=models.CharField(max_length=10, null=True),
        ),
    ]