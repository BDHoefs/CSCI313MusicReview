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
    path('user/<str:pk>', views.user, name='user'),
    path('admin_reports', views.admin_reports, name='admin_reports'),
    path('accent-color-test', views.accent_colors_test, name='accent-colors-test'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
