from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from users.models import Profile
# Create your views here.

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
    context = {'profile': profile}
    return render(request, 'apavelas/card.html', context)

@login_required
def members(request):
    members = Profile.objects.all()
    context = {'members' : members}

    return render(request, 'apavelas/members.html', context)