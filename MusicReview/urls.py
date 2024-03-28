from django.urls import path
from MusicReview import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login, name='logon'),
    path('register', views.register, name='register'),
    path('browse_artists', views.browse_artists, name='browse_artists'),
    path('browse_releases', views.browse_releases, name='browse_releases'),
    path('release/<int:pk>', views.release, name='release'),
    path('artist/<int:pk>', views.artist, name='artist'),
    path('user/<int:pk>', views.user, name='user'),
    path('admin_reports', views.admin_reports, name='admin_reports'),
    path('accent-color-test', views.accent_colors_test, name='accent-colors-test'),
]
