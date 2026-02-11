from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from .models import News, Event, GalleryImage
from .forms import MembershipRequestForm, NewsForm, GalleryImageForm

def home(request):
    news_list = News.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'news_list': news_list})

def about(request):
    return render(request, 'about.html')

def join_club(request):
    if request.method == 'POST':
        form = MembershipRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your membership request has been submitted successfully! We will contact you soon.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = MembershipRequestForm()
    
    return render(request, 'join.html', {'form': form})


# Events View

def events_list(request):
    category = request.GET.get('category')
    if category:
        events = Event.objects.filter(category=category).order_by('date')
    else:
        events = Event.objects.all().order_by('date')
    return render(request, 'events.html', {'events': events, 'selected_category': category})

def gallery(request):
    images = GalleryImage.objects.all().order_by('-created_at')
    return render(request, 'gallery.html', {'images': images})


# Content Management Views

@login_required
@permission_required('club_app.add_news', raise_exception=True)
def manage_content(request):
    return render(request, 'manage_dashboard.html')

@login_required
@permission_required('club_app.add_news', raise_exception=True)
def upload_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            messages.success(request, 'News article uploaded successfully!')
            return redirect('manage_content')
    else:
        form = NewsForm()
    return render(request, 'upload_form.html', {'form': form, 'title': 'Upload News'})

@login_required
@permission_required('club_app.add_galleryimage', raise_exception=True)
def upload_gallery(request):
    if request.method == 'POST':
        form = GalleryImageForm(request.POST, request.FILES)
        if form.is_valid():
            gallery_img = form.save(commit=False)
            gallery_img.author = request.user
            gallery_img.save()
            messages.success(request, 'Image added to gallery successfully!')
            return redirect('manage_content')
    else:
        form = GalleryImageForm()
    return render(request, 'upload_form.html', {'form': form, 'title': 'Upload to Gallery'})

@login_required
def member_dashboard(request):
    return render(request, 'member_dashboard.html', {'user': request.user})
