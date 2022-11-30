from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib import messages
from users.models import Profile
from .models import Benefit, Event, Place, Photo
from .forms import *
from django.core.files.images import ImageFile
# Create your views here.

def emailList(request):
    if request.method == 'POST':
        if 'email_list' in request.POST:
            email = request.POST.get('email_list')
            if EmailList.objects.filter(email=email).exists():
                messages.error(request, 'Correo ya esta en la lista.')
            else:
                EmailList.objects.create(email=email)
                messages.success(request, 'Correo agregado correctamente.')
        

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
    emailList(request)
    if request.method == 'POST':
        if 'login' in request.POST:
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
    emailList(request)
    profile = Profile.objects.filter(user = request.user)[0]
    context = {'profile': profile}
    return render(request, 'apavelas/card.html', context)

def qrscan(request, qrscan):
    emailList(request)
    profile = Profile.objects.filter(id=qrscan)[0]
    if request.method == 'POST':
        if 'login' in request.POST:
            authentication(request)
    context = {'profile': profile}
    return render(request, 'apavelas/card.html', context)

@login_required
def members(request):
    emailList(request)
    members = Profile.objects.all()
    
    context = {'members' : members}

    return render(request, 'apavelas/members.html', context)

def benefits(request):
    emailList(request)
    if request.method == 'POST':
        print(request.POST)
        if 'login' in request.POST:
            authentication(request)
        form = BenefitForm(request.POST, request.FILES)
        if 'new' in request.POST:
            if form.is_valid():
                form.save()
        if 'delete' in request.POST:
            print('delete' , request.POST)
            toBeDeleted = Benefit.objects.get(id=request.POST.get('delete'))
            toBeDeleted.delete()
    benefits = Benefit.objects.all()
    form = BenefitForm()
    context = {'benefits': benefits, 'form': form}
    return render(request, 'apavelas/benefits.html', context)

def places(request, type_of_service):
    emailList(request)
    if request.method == 'POST':
        if 'login' in request.POST:
            authentication(request)
        if 'new' in request.POST:
            print("creating new place", request.POST)
            form = PlacesForm(request.POST, request.FILES)
            if form.is_valid:
                
                form.save()
        if 'delete' in request.POST:
            print('delete' , request.POST)
            toBeDeleted = Place.objects.get(id=request.POST.get('delete'))
            toBeDeleted.delete()

            
    form = PlacesForm()
    places = Place.objects.filter(tipo_de_sitio=type_of_service)
    print(type_of_service, places.count())
    context = {'places': places, 'title': type_of_service, 'form': form}
    return render(request, 'apavelas/places.html', context)

def events(request):
    emailList(request)
    events = Event.objects.all()
    if request.method == 'POST':
        if 'login' in request.POST:
            authentication(request)
        if 'new' in request.POST:
            form=EventsForm(request.POST, request.FILES)
            if form.is_valid:
                form.save()
        if 'delete' in request.POST:
            print('delete' , request.POST)
            toBeDeleted = Event.objects.get(id=request.POST.get('delete'))
            toBeDeleted.delete()
    form = EventsForm()
    context = {'events': events, 'form': form}
    return render(request, 'apavelas/events.html', context)

def gallery(request):
    emailList(request)
    photos = Photo.objects.all()
    if request.method == 'POST':
        if 'login' in request.POST:
            authentication(request)
        if 'new' in request.POST:
            form = GalleryForm(request.POST, request.FILES)
            
            if form.is_valid:
                form.save()
        if 'delete' in request.POST:
            print('delete' , request.POST)
            toBeDeleted = Photo.objects.get(id=request.POST.get('delete'))
            toBeDeleted.delete()
    
    form = GalleryForm(initial={'uploader': request.user.username})
    context = {'photos': photos, 'form': form}
    return render(request, 'apavelas/gallery.html', context)

@login_required
@staff_member_required
def accounting(request):
    emailList(request)
    form = TransactionForm()
    print(request.user)
    profile = Profile.objects.filter(user=request.user)[0]
    if request.method == 'POST':
        if 'new' in request.POST:
            form = TransactionForm(request.POST)
            if form.is_valid:
                form.save()
    # bankAccounts = Bank.objects.all()
    transactions = Transaction.objects.all().order_by('-fecha')
    income = []
    expenses = []
    
    balance = 0
    for i in transactions:
        if i.type_of_transaction == 'INGRESO':
            balance += i.amount
            income.append(i)
        if i.type_of_transaction == 'GASTO':
            balance -= i.amount
            expenses.append(i)
    


    context = {'form': form, 'balance': balance, 'transactions':transactions,
    'income':income, 'expenses':expenses, 'profile':profile}
    return render(request, "apavelas/accounting.html", context)
