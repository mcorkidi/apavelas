from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from users.models import Profile
from .models import Benefit, Event, Place, Photo
from .forms import *
from django.core.files.images import ImageFile
# Create your views here.

def authentication(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        auth = authenticate(request, username=username, password=password)
        if auth:
            login(request, auth)
            messages.success(request, f'Bienvenido {auth.first_name}, iniciaste tu sesión.')
            
        else:
            messages.error(request, "Credenciales invalidos, intenta nuevamente.")
            




def index(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        auth = authenticate(request, username=username, password=password)
        if auth:
            login(request, auth)
            messages.success(request, f'Bienvenido {auth.first_name}, iniciaste tu sesión.')
            return redirect('profile')
        else:
            messages.error(request, "Credenciales invalidos, intenta nuevamente.")
            return redirect('index')

    return render(request, 'apavelas/index.html')


def LogOutView(request):
    logout(request)
    return redirect('index')

@login_required
def card(request):
    profile = Profile.objects.filter(user = request.user)[0]
    context = {'profile': profile}
    return render(request, 'apavelas/card.html', context)

def qrscan(request, qrscan):
    profile = Profile.objects.filter(id=qrscan)[0]
    if request.method == 'POST':
        if 'login' in request.POST:
            authentication(request)
    context = {'profile': profile}
    return render(request, 'apavelas/card.html', context)

@login_required
def members(request):
    members = Profile.objects.all()
    
    context = {'members' : members}

    return render(request, 'apavelas/members.html', context)

def benefits(request):
    benefits = Benefit.objects.all()
    if request.method == 'POST':
        print(request.POST)
        if 'login' in request.POST:
            authentication(request)
        form = BenefitForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            

    form = BenefitForm()
    context = {'benefits': benefits, 'form': form}
    return render(request, 'apavelas/benefits.html', context)

def places(request, type_of_service):
    if request.method == 'POST':
        if 'login' in request.POST:
            authentication(request)
        if 'new' in request.POST:
            print("creating new place", request.POST)
            form = PlacesForm(request.POST, request.FILES)
            if form.is_valid:
                
                form.save()

            
    form = PlacesForm()
    places = Place.objects.filter(tipo_de_sitio=type_of_service)
    print(type_of_service, places.count())
    context = {'places': places, 'title': type_of_service, 'form': form}
    return render(request, 'apavelas/places.html', context)

def events(request):
    events = Event.objects.all()
    if request.method == 'POST':
        if 'login' in request.POST:
            authentication(request)
        if 'new' in request.POST:
            form=EventsForm(request.POST, request.FILES)
            if form.is_valid:
                form.save()
    form = EventsForm()
    context = {'events': events, 'form': form}
    return render(request, 'apavelas/events.html', context)

def gallery(request):
    photos = Photo.objects.all()
    if request.method == 'POST':
        if 'login' in request.POST:
            authentication(request)
    
    form = GalleryForm()
    context = {'photos': photos, 'form': form}
    return render(request, 'apavelas/gallery.html', context)


