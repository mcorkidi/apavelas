from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib import messages
from users.models import Profile
from .models import Benefit, Event, Place
from .forms import *
# from django.core.files.images import ImageFile
from django.conf import settings
import os
from ftplib import FTP
import shutil
from PIL import Image



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
        if 'login' in request.POST:
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
    authentication(request)
    profile = Profile.objects.filter(user = request.user)[0]
    context = {'profile': profile}
    return render(request, 'apavelas/card.html', context)

def qrscan(request, qrscan):
    emailList(request)
    authentication(request)
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
    authentication(request)
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
    authentication(request)
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
    authentication(request)
    events = Event.objects.all().order_by('-created_date')
    if request.method == 'POST':
        if 'login' in request.POST:
            authentication(request)
        if 'new' in request.POST:
            form=EventsForm(request.POST, request.FILES)
            if form.is_valid:
                try:
                    form.save()
                except Exception as e:
                    messages.error(request, f'Error creando evento: {e}')
        if 'delete' in request.POST:
            print('delete' , request.POST)
            toBeDeleted = Event.objects.get(id=request.POST.get('delete'))
            toBeDeleted.delete()
    form = EventsForm()
    context = {'events': events, 'form': form}
    return render(request, 'apavelas/events.html', context)

# def gallery(request):
    # emailList(request)
    # photos = Photo.objects.all()
    # if request.method == 'POST':
    #     if 'login' in request.POST:
    #         authentication(request)
    #     if 'new' in request.POST:
    #         form = GalleryForm(request.POST, request.FILES)
            
    #         if form.is_valid:
    #             form.save()
    #     if 'delete' in request.POST:
    #         print('delete' , request.POST)
    #         toBeDeleted = Photo.objects.get(id=request.POST.get('delete'))
    #         toBeDeleted.delete()
    
    # form = GalleryForm(initial={'uploader': request.user.username})
    # context = {'photos': photos, 'form': form}
    # return render(request, 'apavelas/gallery.html', context)

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
    balance = "{:,.2f}".format(balance)
    


    context = {'form': form, 'balance': balance, 'transactions':transactions,
    'income':income, 'expenses':expenses, 'profile':profile}
    return render(request, "apavelas/accounting.html", context)

@login_required
@staff_member_required
def statement(request):
    transactions = Transaction.objects.all()
    income_accounts = {}
    expense_accounts = {}
    for i in transactions:
        if i.type_of_transaction == "INGRESO":
            if i.account.name not in income_accounts:
                income_accounts[i.account.name] = i.amount
            else:
                print(income_accounts[i.account.name])
                income_accounts[i.account.name] += i.amount
        elif i.type_of_transaction == "GASTO":
            if i.account.name not in expense_accounts:
                expense_accounts[i.account.name] = i.amount
            else:
                expense_accounts[i.account.name] += i.amount
    

    context = {'income_accounts': income_accounts, 'expense_accounts':expense_accounts}
    return render(request, "apavelas/statement.html", context)


def market(request):
    emailList(request)
    authentication(request)
    categories = Category.objects.all()[0:4]
    products = Product.objects.filter(active=True).order_by('-id')[0:6]
    context = {'categories': categories, 'products': products}
    if request.method == 'POST':
        print('request search', request.POST)
        if 'search' in request.POST:
            if request.POST.get('search') == '':
                messages.error(request, "Ingresa lo que buscas. ")
                return render(request,"apavelas/market.html", context)
            return redirect('search_results', keyword=request.POST.get('search'))
    
    
    return render(request,"apavelas/market.html", context)

@login_required
def categoryPick(request):
    emailList(request)
    categories = Category.objects.all()
    if request.method == 'POST':
        print(request.POST)
        if request.POST.get('category') == None:
            messages.error(request, f"Error, es obligatorio seleccionar una categoria para continuar. ")     
        else:
            category = request.POST.get('category')
            print(category)
            return redirect('new_listing',category=category)

    context = {'categories': categories }
    return render(request,"apavelas/market_category_pick.html", context)


@login_required
def newListing(request, category):
    emailList(request)
    def checkForInt(x):
        try:
            int(x)
            print(x)
            return x
        except:
            return 0
    def checkForFloat(x):
        try:
            float(x)
            return x
        except:
            return 0.0

    
    category = Category.objects.filter(name=category)[0]
    if request.method == 'POST':
        if 'next' in request.POST:
            print(request.POST)
            newProduct=Product.objects.create(
                user=request.user, 
                titulo=request.POST.get('titulo'),
                condicion=request.POST.get('condicion'),
                marca=request.POST.get('marca'),
                modelo=request.POST.get('modelo'),
                year=checkForInt(request.POST.get('year')),
                numero_serie=request.POST.get('numero_serie'),
                descripcion=request.POST.get('descripcion'),
                precio=checkForFloat(request.POST.get('precio')),
                entrega=request.POST.get('entrega'),
                costo_envio=request.POST.get('costo_envio'),
                nombre =request.POST.get('nombre'),
                telefono='+' + request.POST.get('pais') + '-' + request.POST.get('telefono'),
                correo =request.POST.get('correo'),
                categoria=category



            )
            newProduct.save()
            return redirect('add_images', product=newProduct)


    context = {'category': category }
    return render(request,"apavelas/market_new_listing.html", context)

@login_required
def addImages(request, product):
    emailList(request)
    user = User.objects.filter(username=request.user)[0]
    product = Product.objects.filter(titulo=product, user = user)[0]
    print(product)
    def handle_uploaded_file(f, filename):
        folder = os.path.join(settings.MEDIA_ROOT, f"products/{request.user.username}")
        if os.path.isdir(folder):
            pass
        else: 
            print(folder)
            os.makedirs(folder)
        with open(os.path.join(folder, f"{filename}"), 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
    if request.method == 'POST':
        
        if request.FILES.getlist('images') != []:
            print("after check", request.FILES.getlist('images'))
            folder = os.path.join(settings.MEDIA_ROOT, f"products/{request.user.username}")
            images = request.FILES.getlist('images')
            images_linkchain = ""
            for i, image in enumerate(images):
                print('Extension', os.path.splitext(image.name)[1])
                filename = str(i) +  os.path.splitext(image.name)[1]
                handle_uploaded_file(image, filename)

                if images_linkchain == "":
                    images_linkchain = settings.FTP_BASE + f'apavelas/{product.id}/{filename}' 
                else: 
                    print(settings.FTP_BASE)
                    print(request.user.username)
                    print(str(image))
                    print(product.images)
                    #Need to fix if user uploads twice same image, it should not be added because it creates a duplicate
                    images_linkchain += f";{settings.FTP_BASE}apavelas/{product.id}/{filename}"
            product.images = images_linkchain
            product.save()
            try:
                with FTP(
                    settings.FTP_DOMAIN,
                    settings.FTP_USER,
                    settings.FTP_PASSWORD
                    ) as ftp:
                    
                    try:
                        ftp.cwd(f'/apavelas/{product.id}')
                    except:
                        print(f"Make FTP Dir apavelas/{product.id}")
                        ftp.mkd(f'apavelas/{product.id}')
                        print("after make dir")
                        ftp.cwd(f'apavelas/{product.id}')
                    # onFTP = ftp.nlst()
                    # print(onFTP)
                    for i in os.listdir(folder):
                        print('starting ftp')
                        file_size = os.path.getsize(f"{folder}/{i}")
                        if file_size > 500000:
                            # Open the image file
                            image = Image.open(f"{folder}/{i}")

                            # Set the maximum size you want the image to be
                            
                            max_size = (1000,1000)
                            # # Resize the image, keeping its aspect ratio
                            image.thumbnail(max_size, Image.ANTIALIAS)

                            # Save the optimized image
                            image.save(f"{folder}/{i}", optimize=True, quality=85)
                        if i == "__MACOSX":
                            pass
                        else:
                            try:
                                with open(os.path.join(folder, i), 'rb') as file:
                                    ftp.storbinary('STOR ' + i, file,102400)     # send the file
                                    print('Uploaded... ' + i, ftp.lastresp)
                                    file.close()
                            except Exception as e:
                                print("error", e)                                   
                shutil.rmtree(folder) 
                return redirect('listing', product_id=product.id)
            except Exception as e:
                print(f"Error in with FTP: {e}")   
                messages.error(request, f"Error subiendo tus imagenes. Intenta nuevamente o contacta al admnistrador. \n {e}")     
        else:
            messages.error(request, f"Estas publicando sin imagenes. Publicaciones con imagen tienen mas chance de que sean compradas.")
            return redirect('listing', product_id=product.id)
    context = {'product': product}
    return render(request, 'apavelas/market_add_images.html', context)



def listing(request, product_id):
    emailList(request)
    authentication(request)
    product = Product.objects.filter(id=product_id)[0]
    images = product.imageList
    categories = Category.objects.all()[0:4]
    if request.method == 'POST':
        print('request search', request.POST)
        if 'search' in request.POST:
            return redirect('search_results', keyword=request.POST.get('search'))

    context = {'product': product, 'images':images, 'categories': categories}
    return render(request, 'apavelas/market_listing.html', context)


def searchResults(request, keyword):
    emailList(request)
    authentication(request)
   
    products = Product.objects.filter(titulo__icontains=keyword, active=True) | Product.objects.filter(marca__icontains=keyword, active=True)\
    | Product.objects.filter(modelo__icontains=keyword, active=True) | Product.objects.filter(year__icontains=keyword, active=True)\
    | Product.objects.filter(categoria=Category.objects.filter(name__icontains=keyword)[0], active=True)
    
    categories = Category.objects.all()[0:4]
    if request.method == 'POST':
        print('request search', request.POST)
        if 'search' in request.POST:
            return redirect('search_results', keyword=request.POST.get('search'))
    context = {'products':products, 'categories':categories}
    return render(request, 'apavelas/market_search.html', context)

@login_required
def myProducts(request):
    emailList(request)
    products = Product.objects.filter(user=User.objects.filter(username=request.user)[0])
    categories = Category.objects.all()[0:4]
    if request.method == 'POST':
        print('request search', request.POST)
        if 'search' in request.POST:
            return redirect('search_results', keyword=request.POST.get('search'))
        elif 'deactivate' in request.POST:
            productToDeactivate = products.filter(id=request.POST.get('deactivate'))[0]
            productToDeactivate.active = False
            productToDeactivate.save()
        elif 'activate' in request.POST:
            productToActivate = products.filter(id=request.POST.get('activate'))[0]
            productToActivate.active = True
            productToActivate.save()
        elif 'delete' in request.POST:
            products.filter(id=request.POST.get('delete')).delete()
    
    context = {'products':products, 'categories':categories}
    return render(request, 'apavelas/market_my_products.html', context)

@login_required
def editListing(request, product_id):
    
    emailList(request)
    def checkForInt(x):
        print(x)
        try:
            int(x)
            print(x)
            return x
        except:
            return 0
    def checkForFloat(x):
        try:
            float(x)
            return x
        except:
            return 0.0
    product = Product.objects.filter(id=product_id, user=User.objects.filter(username=request.user)[0])[0]
    images = product.imageList
    imageList = [x for x in (product.images).split(";") ]
    print(imageList)
    categories = Category.objects.all()
    if request.method == 'POST':
        print(request.POST)
        if 'search' in request.POST:
            return redirect('search_results', keyword=request.POST.get('search'))
        elif 'update' in request.POST:
            def handle_uploaded_file(f, filename):
                folder = os.path.join(settings.MEDIA_ROOT, f"products/{request.user.username}")
                if os.path.isdir(folder):
                    pass
                else: 
                    print(folder)
                    os.makedirs(folder)
                with open(os.path.join(folder, f"{filename}"), 'wb+') as destination:
                        for chunk in f.chunks():
                            destination.write(chunk)
            if request.FILES.getlist('new_images') != []:
                
                folder = os.path.join(settings.MEDIA_ROOT, f"products/{request.user.username}")
                new_images = request.FILES.getlist('new_images')
                images_linkchain = product.images
                for i, new_image in enumerate(new_images):
                    print('DEBUG>>>>>>> adding edit image')
                    filename = str(i) +  os.path.splitext(new_image.name)[1]
                    handle_uploaded_file(new_image, filename)
                    if images_linkchain == "":
                        images_linkchain = settings.FTP_BASE + f'apavelas/{product.id}/{filename}' 
                    else: 
                        images_linkchain += f";{settings.FTP_BASE}apavelas/{product.id}/{filename}"
                    product.images = images_linkchain
                    product.save()
                    try:
                        with FTP(
                            settings.FTP_DOMAIN,
                            settings.FTP_USER,
                            settings.FTP_PASSWORD
                            ) as ftp:
                            print('uploading image')
                            try:
                                ftp.cwd(f'/apavelas/{product.id}')
                            except:
                                print(f"Make FTP Dir apavelas/{product.id}")
                                ftp.mkd(f'apavelas/{product.id}')
                                print("after make dir")
                                ftp.cwd(f'apavelas/{product.id}')
                            # onFTP = ftp.nlst()
                            # print(onFTP)
                            for i in os.listdir(folder):
                                print('starting ftp')
                                file_size = os.path.getsize(f"{folder}/{i}")
                                if file_size > 500000:
                                    # Open the image file
                                    image = Image.open(f"{folder}/{i}")
                                    # Set the maximum size you want the image to be
                                    max_size = (1000,1000)
                                    # # Resize the image, keeping its aspect ratio
                                    image.thumbnail(max_size, Image.ANTIALIAS)
                                    # Save the optimized image
                                    image.save(f"{folder}/{i}", optimize=True, quality=85)
                                if i == "__MACOSX":
                                    pass
                                else:
                                    try:
                                        with open(os.path.join(folder, i), 'rb') as file:
                                            ftp.storbinary('STOR ' + i, file,102400)     # send the file
                                            print('Uploaded... ' + i, ftp.lastresp)
                                            file.close()
                                    except Exception as e:
                                        print("error", e) 
                                        messages.error(request, f"Error subiendo tus imagenes. Intenta nuevamente o contacta al admnistrador. \n {e}")  
                                    
                        shutil.rmtree(folder) 
                    except Exception as e:
                        print(f"Error in with FTP: {e}")   
                        messages.error(request, f"Error subiendo tus imagenes. Intenta nuevamente o contacta al admnistrador. \n {e}")  

            print('Category>>>>>>>>', request.POST)
            
            product.titulo=request.POST.get('titulo')
            product.condicion=request.POST.get('condicion')
            product.marca=request.POST.get('marca')
            product.modelo=request.POST.get('modelo')
            product.year=checkForInt(request.POST.get('year'))
            product.numero_serie=request.POST.get('numero_serie')
            product.descripcion=request.POST.get('descripcion')
            product.precio=checkForFloat(request.POST.get('precio'))
            product.entrega=request.POST.get('entrega')
            product.costo_envio=request.POST.get('costo_envio')
            product.nombre =request.POST.get('nombre')
            product.telefono=request.POST.get('telefono')
            product.correo =request.POST.get('correo')
            product.categoria = Category.objects.filter(name=request.POST.get('new_category'))[0]
           
            product.save()
            return redirect('listing', product_id=product.id)
        elif 'delete_image' in request.POST:
            imagePath =  request.POST.get('delete_image')
            imageDelete = imagePath.split('/')[-1]
            print(imageDelete)
            imageList.remove(imagePath)
            product.images = ';'.join(imageList)
            product.save()
            with FTP(
                settings.FTP_DOMAIN,
                settings.FTP_USER,
                settings.FTP_PASSWORD
                ) as ftp:
                try:
                    ftp.cwd(f'apavelas/{product.id}')
                    ftp.delete(imageDelete)
                    ftp.close()
                    print("-----Deleting image-------")
                    
                    
                except Exception as e:
                    print(f"FTP Directory not found, error: {e}")
                    messages.error(request, "Error eliminando imagen.")
                    context = {'product': product, 'images':images, 'categories': categories}
                    return render(request, 'apavelas/market_edit_listing.html', context)
        
            
    context = {'product': product, 'images':images, 'categories': categories}
    
    return render(request, 'apavelas/market_edit_listing.html', context)