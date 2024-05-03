from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from MusicReview import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.logon, name='logon'),
    path('logout', views.logoff, name='logout'),
    path('register', views.register, name='register'),
    path('browse_artists', views.browse_artists, name='browse_artists'),
    path('browse_releases', views.browse_releases, name='browse_releases'),
    path('add_artist', views.add_artist, name='add_artist'),
    path('add_release', views.add_release, name='add_release'),
    path('search', views.search, name='search'),
    path('release/<int:pk>', views.release, name='release'),
    path('release_add_track/<int:pk>', views.release_add_track, name='release_add_track'),
    path('artist/<int:pk>', views.artist, name='artist'),
    path('report_release/<int:pk>', views.report_release, name='report_release'),
    path('report_review/<int:release_pk>/<int:review_pk>', views.report_review, name='report_review'),
    path('report_artist/<int:artist_pk>', views.report_artist, name='report_artist'),
    path('user/<str:pk>', views.user, name='user'),
    path('admin_reports', views.admin_reports, name='admin_reports'),
    path('delete_release/<int:release_pk>', views.delete_release, name='delete_release'),
    path('delete_review/<int:review_pk>', views.delete_review, name='delete_review'),
    path('delete_artist/<int:artist_pk>', views.delete_artist, name='delete_artist'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
