from pickletools import optimize
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from users.models import Profile
from apavelas.models import Transaction
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import qrcode
from django.conf import settings
from os.path import exists
from .forms import *
from PIL import Image, ExifTags
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


# Create your views here.

def register(request):
    if request.method == 'POST':
        if 'register' in request.POST:
            print(request.POST)
            username = request.POST.get('username')
            email =request.POST.get('email')
            password = request.POST.get('password')
            password1 = request.POST.get('password1')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            telephone = request.POST.get('telephone')
            sport = request.POST.get('sport')
            talla = request.POST.get('talla')
            if password != password1:
                messages.error(request, 'Error, revisa que la contraseña sea igual a la confirmacion.')
                return render(request, 'users/registration.html')
            try:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Error: Correo ya registrado, intenta nuevamente con otro correo.')
                    return render(request, 'users/registration.html')
                newUser = User.objects.create_user(username, email, password)
                newUser.first_name = first_name
                newUser.last_name = last_name
                newUser.save()
            except:
                messages.error(request, 'Error en el registro intenta nuevamente con otro usuario.')
                return render(request, 'users/registration.html')

            newProfile = Profile.objects.create(user=newUser, telephone=telephone, 
            sport=sport, talla=talla) 
            newProfile.qrcode = f'{settings.BASE_HOST}qrscan/{newProfile.id}' 
            newProfile.save()
            img = qrcode.make(f'{settings.BASE_HOST}qrscan/{newProfile.id}')

            
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
    
    profile = Profile.objects.get(user = User.objects.get(username=request.user))
    transactions = Transaction.objects.filter(user = User.objects.get(username=request.user))
    if exists(f"{settings.MEDIA_ROOT}/qrcodes/{profile.id}.jpg"):
        ...
    else:
        profile.qrcode = f'{settings.BASE_HOST}qrscan/{profile.id}' 
        profile.save()
        img = qrcode.make(f'{settings.BASE_HOST}qrscan/{profile.id}')

        
        img.save(f'{settings.MEDIA_ROOT}/qrcodes/{profile.id}.jpg')
    if request.method == 'POST':
        print(request.POST)
    

        form=ProfileImageForm(request.POST, request.FILES)
        face_form = FaceImageForm(request.POST, request.FILES)
        if form.is_valid():
            

            img = form.cleaned_data.get('foto_perfil')
            optImage = Image.open(img)
            for orientation in ExifTags.TAGS.keys() :
                    if ExifTags.TAGS[orientation]=='Orientation' : break
            exif=dict(optImage._getexif().items())
            if exif[orientation] == 3 :
                optImage=optImage.rotate(180, expand=True)
            elif exif[orientation] == 6 :
                optImage=optImage.rotate(270, expand=True)
            elif exif[orientation] == 8 :
                optImage=optImage.rotate(90, expand=True)
            thumb_io = BytesIO()
            optImage.save(thumb_io, format='JPEG', quality=50)
            
            inmemory_uploaded_file = InMemoryUploadedFile(thumb_io, None, f'{profile.user.username}_profile.jpeg', 
                                              'image/jpeg', thumb_io.tell(), None)
            
            profile.image = inmemory_uploaded_file
            profile.save()

        if face_form.is_valid():
           
            face_img = face_form.cleaned_data.get('foto_tarjeta')
            optImage = Image.open(face_img)
            for orientation in ExifTags.TAGS.keys() :
                    if ExifTags.TAGS[orientation]=='Orientation' : break
            exif=dict(optImage._getexif().items())
            if exif[orientation] == 3 :
                optImage=optImage.rotate(180, expand=True)
            elif exif[orientation] == 6 :
                optImage=optImage.rotate(270, expand=True)
            elif exif[orientation] == 8 :
                optImage=optImage.rotate(90, expand=True)
            thumb_io = BytesIO()
            optImage.save(thumb_io, format='JPEG', quality=50)
            inmemory_uploaded_file = InMemoryUploadedFile(thumb_io, None, f'{profile.user.username}_face.jpeg', 
                                              'image/jpeg', thumb_io.tell(), None)
            profile.faceImage = inmemory_uploaded_file
            profile.save()
        if 'edit' in request.POST:
            username = request.POST.get('username')
            email =request.POST.get('email')
            password = request.POST.get('password')
            password1 = request.POST.get('password1')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            telephone = request.POST.get('telephone')
            sport = request.POST.get('sport')
            talla = request.POST.get('talla')
            
            
            if password == '' and password1 == '':
                editUser = request.user
                editUser.username = username
                editUser.email = email
                editUser.first_name = first_name
                editUser.last_name = last_name
                editUser.save()
                editProfile = Profile.objects.get(user=editUser)
                editProfile.telephone = telephone
                editProfile.sport = sport
                editProfile.talla = talla
                if talla == 'Selecciona...':
                    editProfile.talla = profile.talla
                if sport == 'Selecciona...':
                    editProfile.sport = profile.sport
                editProfile.save()
                profile = editProfile
                messages.success(request, 'Perfil editado exitosamente!')
            else:
                if password != password1:
                    messages.error(request, 'Error, revisa que la contraseña sea igual a la confirmacion.')
                else:
                    editUser = request.user
                    editUser.username = username
                    editUser.email = email
                    editUser.first_name = first_name
                    editUser.last_name = last_name
                    editUser.password = password
                    editUser.save()
                    editProfile = Profile.objects.get(user=editUser)
                    editProfile.telephone = telephone
                    editProfile.sport = sport
                    editProfile.talla = talla
                    if talla == 'Selecciona...':
                        editProfile.talla = profile.talla
                    if sport == 'Selecciona...':
                        editProfile.sport = profile.sport
                    editProfile.save()
                    messages.success(request, 'Perfil editado exitosamente!')
                    profile = editProfile
        

    else:
        form = ProfileImageForm()
        face_form = FaceImageForm()
      



    context = {'profile': profile, 'form':form, 'face_form':face_form, 'transactions': transactions}


    return render(request, 'users/profile.html', context)

