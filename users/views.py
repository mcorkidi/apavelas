from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from users.models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import qrcode
from django.conf import settings
import os
from .forms import ProfileImageForm, FaceImageForm


# Create your views here.

def register(request):
    if request.method == 'POST':
        print(request.POST)
        username = request.POST.get('username')
        email =request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        telephone = request.POST.get('telephone')
        sport = request.POST.get('sport')
        if password != password1:
            messages.error(request, 'Error, revisa que la contraseña sea igual a la confirmacion.')
            return render(request, 'users/registration.html')
        try:
            newUser = User.objects.create_user(username, email, password)
            newUser.first_name = first_name
            newUser.last_name = last_name
            newUser.save()
        except:
            messages.error(request, 'Error en el registro intenta nuevamente con otro usuario.')
            return render(request, 'users/registration.html')

        newProfile = Profile.objects.create(user=newUser, telephone=telephone, 
        sport=sport)
        newProfile.qrcode = f'{settings.BASE_HOST}{newProfile.id}' 
        newProfile.save()
        img = qrcode.make(f'{settings.BASE_HOST}{newProfile.id}')

        
        img.save(f'{settings.MEDIA_ROOT}/qrcodes/{newProfile.id}.jpg')


        messages.success(request, 'Te registraste exitosamente, procede a iniciar la sesión.')
        auth = authenticate(request, username=username, password=password)
        if auth:
            login(request, auth)
            messages.success(request, f'Bienvenido {auth.first_name}, iniciaste tu sesión.')
            return redirect('profile')
        else:
            messages.error(request, "Credenciales invalidos, intenta nuevamente.")
            return redirect('index')



    return render(request, 'users/registration.html')

@login_required
def profile(request):
    profile = Profile.objects.filter(user = request.user)[0]

    if request.method == 'POST':
        print(request.POST)
    

        form=ProfileImageForm(request.POST, request.FILES)
        face_form = FaceImageForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.cleaned_data.get('foto_perfil')
            profile.image=img
            profile.save()
        if face_form.is_valid():
            face_img = face_form.cleaned_data.get('foto_tarjeta')
            profile.faceImage=face_img
            profile.save()
    else:
        form = ProfileImageForm()
        face_form = FaceImageForm()



    context = {'profile': profile, 'form':form, 'face_form':face_form}


    return render(request, 'users/profile.html', context)

