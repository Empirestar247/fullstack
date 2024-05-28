from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, TrackingForm
from .models import Tracking
from django.core.paginator import Paginator
from .forms import UserRegisterForm, TrackingForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('service-home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def update_tracking_id(request):
    try:
        instance = Tracking.objects.get(user=request.user)
    except Tracking.DoesNotExist:
        instance = None

    if request.method == 'POST':
        form = TrackingForm(request.POST, instance=instance)
        if form.is_valid():
            tracking = form.save(commit=False)
            tracking.user = request.user
            tracking.save()
            return redirect('some-view')
    else:
        form = TrackingForm(instance=instance)
    return render(request, 'update_tracking_id.html', {'form': form})

def delete_tracking_info(request):
    Tracking.objects.filter(user=request.user).delete()
    return redirect('some-view')

def display_tracking_info(request):
    tracking_info_list = Tracking.objects.filter(user=request.user)
    paginator = Paginator(tracking_info_list, 5)  # Show 5 tracking info per page.

    page_number = request.GET.get('page')
    tracking_info = paginator.get_page(page_number)

    return render(request, 'display_tracking_info.html', {'tracking_info': tracking_info})


def search(request):
    query = request.GET.get('q')
    results = Tracking.objects.filter(tracking_id__icontains=query)
    return render(request, 'search_results.html', {'results': results})

# Path: logistic/users/views.py
def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def track(request):
    if request.method == 'POST':
        form = TrackingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TrackingForm()
    return render(request, 'track.html', {'form': form})