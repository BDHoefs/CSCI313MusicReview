from django.contrib import admin

from .models import Artist, Song, Review, Release, ReportArtistInfo, ReportReviewContent, ReportReleaseInfo

# Register your models here.
admin.site.register(Artist)
admin.site.register(Song)
admin.site.register(Review)
admin.site.register(Release)
admin.site.register(ReportArtistInfo)
admin.site.register(ReportReviewContent)
admin.site.register(ReportReleaseInfo)