from datetime import timedelta

from django.shortcuts import render, redirect
from django.views.decorators.csrf import requires_csrf_token
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone

from PIL import Image

from .accent_colors import default_colors, calculate_accent_colors
from .forms import ImageColorForm, SearchForm, CreateUserForm, LoginForm, ReviewForm, ReleaseForm, TrackForm, ReleaseSort, ArtistForm, ReportReleaseInfo, ReportReviewForm, ReportReleaseForm
from .models import Artist, Release, Review, ReportReleaseInfo, ReportArtistInfo, ReportReviewContent, Artist

def get_ctx(request, release=None):
    ctx = { 'searchForm': SearchForm() }
    if release is not None:
        ctx['accentColors'] = [release.accent_color1, release.accent_color2, release.accent_color3, release.accent_color4]
    else:
        ctx['accentColors'] = default_colors()
    if request.user.is_authenticated:
        ctx['userName'] = request.user.username

    
    ctx['superuser'] = request.user.is_superuser

    return ctx

def release_ctx(request, release):
    ctx = get_ctx(request, release=release)
    ctx['release'] = release

    # Formats the 'genres' field into a simple comma separated list
    ctx['genres'] = ', '.join([s.strip("'") for s in release.genres.strip('[]').split(', ')])

    songs = release.songs.all()
    song_lengths = [(song.title, str(timedelta(seconds=song.length)).lstrip('0:')) for song in songs if song.length is not None]
    ctx['songLengths'] = song_lengths

    ctx['artists'] = ', '.join([artist.name for artist in release.artists.all()])

    reviews = release.reviews.all()
    ctx['reviews'] = reviews

    return ctx

def home(request):
    ctx = get_ctx(request)
    return render(request, 'index.html', context = ctx)

def logon(request):
    ctx = get_ctx(request)

    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                ctx['errMessages'] = ['Username or password incorrect']

    ctx['loginForm'] = form
    return render(request, 'accounts/login.html', context = ctx)

def logoff(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect('home')

def register(request):
    ctx = get_ctx(request)

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            ctx['errMessages'] = ["Passwords don't match"]

    ctx['registerForm'] = form
    return render(request, 'accounts/register.html', context = ctx)

def browse_artists(request):
    ctx = get_ctx(request)
    sort = 'Recently added'

    if request.method == 'POST':
        sort_form = ReleaseSort(request.POST)
        if sort_form.is_valid():
            sort = sort_form.cleaned_data['sort']

    sort_form = ReleaseSort()
    ctx['sortForm'] = sort_form

    if sort == 'Recently added':
        ctx['artists'] = Artist.objects.order_by('time_added')[:100]
    elif sort == 'Recently reviewed':
        ctx['artists'] = Artist.objects.order_by('last_reviewed')[:100]

    if ctx['artists'] is not None:
        releases = ctx['artists']
        ctx['artists'] = [releases[i:i+3] for i in range(0, len(releases), 3)]

    print(ctx['artists'])
    return render(request, 'music/browse_artists.html', context = ctx)

def browse_releases(request):
    ctx = get_ctx(request)
    sort = 'Recently added'

    if request.method == 'POST':
        sort_form = ReleaseSort(request.POST)
        if sort_form.is_valid():
            sort = sort_form.cleaned_data['sort']

    sort_form = ReleaseSort()
    ctx['sortForm'] = sort_form

    if sort == 'Recently added':
        ctx['releases'] = Release.objects.order_by('time_added')[:100]
    elif sort == 'Recently reviewed':
        ctx['releases'] = Release.objects.order_by('last_reviewed')[:100]

    # Turn releases into a 2d array with 3 elements per row
    if ctx['releases'] is not None:
        releases = ctx['releases']
        ctx['releases'] = [releases[i:i+3] for i in range(0, len(releases), 3)]

    print(ctx['releases'])

    return render(request, 'music/browse_releases.html', context = ctx)

def add_artist(request):
    ctx = get_ctx(request)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('register')
        artist_form = ArtistForm(request.POST, request.FILES)
        if artist_form.is_valid():
            image = Image.open(artist_form.cleaned_data['artist_photo'])
            accent_colors = calculate_accent_colors(image)

            artist = artist_form.save(commit=False)
            artist.accent_color1 = accent_colors[0]
            artist.accent_color2 = accent_colors[1]
            artist.accent_color3 = accent_colors[2]
            artist.accent_color4 = accent_colors[3]
            artist.time_added = timezone.now()
            artist.added_by = request.user
            artist.save()

            return redirect('artist', pk=artist.pk)
        
    ctx['artistForm'] = ArtistForm()
    return render(request, 'music/add_artist.html', context = ctx)

def add_release(request):
    ctx = get_ctx(request)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('register')
        release_form = ReleaseForm(request.POST, request.FILES)
        if release_form.is_valid(): 
            image = Image.open(release_form.cleaned_data['cover_art'])
            accent_colors = calculate_accent_colors(image)

            release = release_form.save(commit=False)
            release.accent_color1 = accent_colors[0]
            release.accent_color2 = accent_colors[1]
            release.accent_color3 = accent_colors[2]
            release.accent_color4 = accent_colors[3]
            release.time_added = timezone.now()
            release.added_by = request.user
            release.save()
            release.artists.set(release_form.cleaned_data['artists'])

            return redirect('release', pk=release.pk)


    ctx['releaseForm'] = ReleaseForm()
    return render(request, 'music/add_release.html', context = ctx)

def search(request):
    ctx = get_ctx(request)
    query = request.GET.get('search')
    releases = []

    if query:
        releases = Release.objects.filter(title__icontains=query)

    ctx['releases'] = releases
    return render(request, 'music/search.html', context=ctx)

def release(request, pk):
    release = Release.objects.get(pk=pk)    
    ctx = release_ctx(request, release)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('register')
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.time = timezone.now()
            review.save()

            release.reviews.add(review)
            release.last_reviewed = timezone.now()
            release.save()
            # Redirect because ctx['reviews'] is now out of date
            return redirect('release', pk=pk)
        else:
            ctx['errMessages'] = ['Error submitting review']

    ctx['reviewForm'] = ReviewForm()

    return render(request, 'music/release.html', context = ctx)

def release_add_track(request, pk):
    release = Release.objects.get(pk=pk)    
    ctx = release_ctx(request, release)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('register')
        track_form = TrackForm(request.POST)
        if track_form.is_valid():
            track = track_form.save()
            release.songs.add(track)
            return redirect('release', pk=pk)
        else:
            ctx['errMessages'] = ['Error submitting track']

    ctx['trackForm'] = TrackForm()

    return render(request, 'music/release.html', context=ctx)

def artist(request, pk):
    artist = Artist.objects.get(pk=pk)
    reviewForm = ReviewForm()
    ctx = get_ctx(request)  # Get the common context
    ctx['artist'] = artist
    releases = artist.release_set.all()
    ctx['releases'] = [releases[i:i+3] for i in range(0, len(releases), 3)]
    return render(request, 'music/artist.html', context=ctx)

def report_release(request, pk):
    release = Release.objects.get(pk=pk)    
    ctx = release_ctx(request, release)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('register')
        report_form = ReportReleaseForm(request.POST)
        if report_form.is_valid():
            report = report_form.save(commit = False)
            report.release = release
            report.reported_by = request.user
            report.report_time = timezone.now()
            report.save()
            
            return redirect('release', pk=pk)
        else:
            ctx['errMessages'] = ['Error submitting report']

    ctx['reportReleaseForm'] = ReportReleaseForm()

    return render(request, 'music/release.html', context = ctx)

def report_review(request, release_pk, review_pk):
    release = Release.objects.get(pk=release_pk)
    review = Review.objects.get(pk=review_pk)
    ctx = release_ctx(request, release)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('register')
        report_form = ReportReviewForm(request.POST)
        if report_form.is_valid():
            report = report_form.save(commit = False)
            report.review = review
            report.reported_by = request.user
            report.report_time = timezone.now()
            report.save()

            return redirect('release', pk=release_pk)
        else:
            ctx['errMessages'] = ['Error submitting report']

    ctx['reportReview'] = review
    ctx['reportReviewForm'] = ReportReviewForm()

    return render(request, 'music/release.html', context = ctx)

def user(request, pk):
    ctx = get_ctx(request)
    # View logic here
    return render(request, 'accounts/user.html', context = ctx)

def admin_reports(request):
    ctx = get_ctx(request)
    # Validate that the user is an admin
    # View logic here
    ctx['releaseReports'] = ReportReleaseInfo.objects.all()
    ctx['reviewReports'] = ReportReviewContent.objects.all()
    ctx['artistReports'] = ReportArtistInfo.objects.all()
    return render(request, 'admin/reports.html', context = ctx)

def delete_release(request, release_pk):
    if request.user is not None:
        if request.user.is_superuser:
            release = Release.objects.get(pk = release_pk)
            release.delete()
    return redirect('admin_reports')

def delete_review(request, review_pk):
    if request.user is not None:
        if request.user.is_superuser:
            review = Review.objects.get(pk = review_pk)
            review.delete()
    return redirect('admin_reports')

def delete_artist(request, artist_pk):
    if request.user is not None:
        if request.user.is_superuser:
            artist = Artist.objects.get(pk = artist_pk)
            artist.delete()
    return redirect('admin_reports')

def accent_colors_test(request):
    ctx = get_ctx(request)
    ctx['imageForm'] = ImageColorForm()
    if request.method == 'POST':
        ctx['imageForm'] = ImageColorForm(request.POST, request.FILES)
        if ctx['imageForm'].is_valid():
            image = Image.open(ctx['imageForm'].cleaned_data['image'])
            ctx['accentColors'] = calculate_accent_colors(image)

    return render(request, 'accent_colors.html', ctx)

def userPage(request, release):
    ctx = get_ctx(request)
    
    return render(request, 'accounts/user?page.html', context = ctx)