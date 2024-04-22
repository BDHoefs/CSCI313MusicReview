from datetime import timedelta
from statistics import mean

from django.shortcuts import render, redirect
from django.views.decorators.csrf import requires_csrf_token
from django.contrib.auth import authenticate, login, logout

from PIL import Image

from .accent_colors import default_colors, calculate_accent_colors
from .forms import ImageColorForm, SearchForm, CreateUserForm, LoginForm
from .models import Release

def get_ctx(request):
    ctx = { "accentColors": default_colors(), "searchForm": SearchForm() }
    if request.user.is_authenticated:
        ctx["userName"] = request.user.username

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
                ctx["errMessages"] = ["Username or password incorrect"]

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
    # View logic here
    return render(request, 'music/browse_artists.html', context = ctx)

def browse_releases(request):
    ctx = get_ctx(request)
    # View logic here
    return render(request, 'music/browse_releases.html', context = ctx)

@requires_csrf_token
def search(request):
    ctx = get_ctx(request)
    # View logic here
    return render(request, 'music/search.html', context = ctx)

# CSRF Token because a user may submit forms to this view to update and add information to the release or submit reports
@requires_csrf_token
def release(request, pk):
    ctx = get_ctx(request)

    release = Release.objects.get(pk=pk)
    ctx["release"] = release

    songs = release.songs.all()
    song_lengths = [(song.title, str(timedelta(seconds=song.length)).lstrip("0:")) for song in songs if song.length is not None]
    ctx["songLengths"] = song_lengths

    ctx["artists"] = ', '.join([artist.name for artist in release.artists.all()])

    reviews = release.reviews.all()
    ctx["reviews"] = reviews
    if reviews.count() > 0:
        ctx["averageRating"] = str(mean([review.score for review in reviews])) + '/10'
    else:
        ctx["averageRating"] = "Not reviewed yet"

    return render(request, 'music/release.html', context = ctx)

# CSRF Token because a user may submit forms to this view to update and add information to the artist or submit reports
@requires_csrf_token
def artist(request, pk):
    ctx = get_ctx(request)
    # View logic here
    return render(request, 'music/artist.html', context = ctx)

def user(request, pk):
    ctx = get_ctx(request)
    # View logic here
    return render(request, 'accounts/user.html', context = ctx)

# CSRF Token because the admin may submit forms to this view to make content moderation decisions
@requires_csrf_token
def admin_reports(request):
    ctx = { "userId": 0, "accentColors": default_colors(), "searchForm": SearchForm() }
    # Validate that the user is an admin
    # View logic here
    return render(request, 'admin/reports.html', context = ctx)

@requires_csrf_token
def accent_colors_test(request):
    ctx = get_ctx(request)
    ctx["imageForm"] = ImageColorForm()
    if request.method == "POST":
        ctx["imageForm"] = ImageColorForm(request.POST, request.FILES)
        if ctx["imageForm"].is_valid():
            image = Image.open(ctx["imageForm"].cleaned_data["image"])
            ctx["accentColors"] = calculate_accent_colors(image)

    return render(request, 'accent_colors.html', ctx)
