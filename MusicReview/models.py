from django.db import models
from django.contrib.auth.models import User

class Artist(models.Model):
    name = models.CharField(max_length = 100)
    cover_art = models.ImageField(upload_to="artists", null=True)
    time_added = models.DateTimeField() # For sorting by recent in the browse artists page
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) # When a user account is deleted we don't want the info they added to also be deleted

class Song(models.Model):
    title = models.CharField(max_length = 100)
    length = models.IntegerField(null = True) # Song length in seconds
    is_explicit = models.BooleanField(),
    artists = models.ManyToManyField(Artist)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

class Review(models.Model):
    content = models.TextField(blank=True)
    score = models.IntegerField() # 0 - 10 score
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField()

class Release(models.Model):
    title = models.CharField(max_length = 100)
    cover_art = models.ImageField(upload_to="cover_art")
    release_type = models.CharField(max_length = 100)
    genres = models.CharField(max_length = 1000)
    is_explicit = models.BooleanField()
    songs = models.ManyToManyField(Song)
    artists = models.ManyToManyField(Artist)
    reviews = models.ManyToManyField(Review, blank=True)
    last_reviewed = models.DateTimeField(blank=True, null=True) # For sorting by last reviewed in the browse page
    time_added = models.DateTimeField() # For sorting by recent in the browse page
    released = models.DateField(null=True),
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) 
    accent_color1 = models.CharField(max_length = 10, blank=True) # Stored as a hex string. Ex. #FFFFFF
    accent_color2 = models.CharField(max_length = 10, blank=True) 
    accent_color3 = models.CharField(max_length = 10, blank=True) 
    accent_color4 = models.CharField(max_length = 10, blank=True) 

class ReportArtistInfo(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    report_text = models.TextField()
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    report_time = models.DateTimeField(),

class ReportSongInfo(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    report_text = models.TextField()
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    report_time = models.DateTimeField(),

class ReportReviewContent(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    report_text = models.TextField()
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    report_time = models.DateTimeField(),

class ReportReleaseInfo(models.Model):
    release = models.ForeignKey(Release, on_delete=models.CASCADE)
    report_text = models.TextField()
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    report_time = models.DateTimeField(),
