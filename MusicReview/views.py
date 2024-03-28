from django.shortcuts import render
from django.views.decorators.csrf import requires_csrf_token

from PIL import Image

from .accent_colors import default_colors, calculate_accent_colors
from .forms import ImageColorForm

def home(request):
    ctx = { "userId": 0, "accentColors": default_colors() }
    return render(request, 'index.html', context = ctx)

@requires_csrf_token
def login(request):
    ctx = { "userId": 0, "accentColors": default_colors() }
    # View logic here
    return render(request, 'accounts/login.html', context = ctx)

@requires_csrf_token
def register(request):
    ctx = { "userId": 0, "accentColors": default_colors() }
    # View logic here
    return render(request, 'accounts/register.html', context = ctx)

def browse_artists(request):
    ctx = { "userId": 0, "accentColors": default_colors() }
    # View logic here
    return render(request, 'music/browse_artists.html', context = ctx)

def browse_releases(request):
    ctx = { "userId": 0, "accentColors": default_colors() }
    # View logic here
    return render(request, 'music/browse_releases.html', context = ctx)

# CSRF Token because a user may submit forms to this view to update and add information to the release or submit reports
@requires_csrf_token
def release(request, pk):
    ctx = { "userId": 0, "accentColors": default_colors() }
    # View logic here
    return render(request, 'music/release.html', context = ctx)

# CSRF Token because a user may submit forms to this view to update and add information to the artist or submit reports
@requires_csrf_token
def artist(request, pk):
    ctx = { "userId": 0, "accentColors": default_colors() }
    # View logic here
    return render(request, 'music/artist.html', context = ctx)

def user(request, pk):
    ctx = { "userId": 0, "accentColors": default_colors() }
    # View logic here
    return render(request, 'accounts/user.html', context = ctx)

# CSRF Token because the admin may submit forms to this view to make content moderation decisions
@requires_csrf_token
def admin_reports(request):
    ctx = { "userId": 0, "accentColors": default_colors() }
    # Validate that the user is an admin
    # View logic here
    return render(request, 'admin/reports.html', context = ctx)

@requires_csrf_token
def accent_colors_test(request):
    ctx = { "userId": 0, "accentColors": default_colors(), "form": ImageColorForm() }
    if request.method == "POST":
        ctx["form"] = ImageColorForm(request.POST, request.FILES)
        if ctx["form"].is_valid():
            image = Image.open(ctx["form"].cleaned_data["image"])
            ctx["accentColors"] = calculate_accent_colors(image)

    return render(request, 'accent_colors.html', ctx)
