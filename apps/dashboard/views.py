from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ProfileForm
from django.contrib.auth.models import User

from .models import Profile, Bitacora
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone
from django.http import HttpResponse
from openpyxl import Workbook
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def dashboard(request):
    return render (request, 'dashboard.html')

@login_required
def bitacora(request):
    # Initialize variables with default values
    profiles = None
    bitacoras = None
    search_query = request.GET.get('filter', '')
    search_bitacora = request.GET.get('filter', '')  # Same filter for both or separate if needed
    
    # Initialize querysets
    profile_list = Profile.objects.all().order_by('name')
    bitacora_list = Bitacora.objects.all().order_by('-fecha')
    
    # Profile filtering
    if search_query:
        profile_list = profile_list.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query)
        )
        
        paginator = Paginator(profile_list, 5)
        page_number = request.GET.get('page')
        profiles = paginator.get_page(page_number)
    
    # Bitacora filtering
    if search_bitacora:
        bitacora_list = bitacora_list.filter(
            # Add your Bitacora model filter conditions here
            # Example: Q(action__icontains=search_bitacora) | Q(user__name__icontains=search_bitacora)
        )
        
        paginator = Paginator(bitacora_list, 5)
        page_number = request.GET.get('page')
        bitacoras = paginator.get_page(page_number)
    
    # If no search was performed, show all results
    if not search_query and not search_bitacora:
        paginator = Paginator(profile_list, 5)
        page_number = request.GET.get('page')
        profiles = paginator.get_page(page_number)
        
        paginator = Paginator(bitacora_list, 5)
        page_number = request.GET.get('page')
        bitacoras = paginator.get_page(page_number)
    
    context = {
        'bitacoras': bitacoras,
        'profiles': profiles,
        'search_query': search_query,
        'search_bitacora': search_bitacora
    }
    
    return render(request, 'bitacora.html', context)

@login_required
def profile(request):
    profile = Profile.objects.first()
    
    if request.method == 'POST':
        profile = ProfileForm(request.POST, request.FILES)
        if profile.is_valid():
            new_profile = profile.save(commit=False)
            print(request.POST, request.FILES)
            new_profile.save()  #Guarda en la bsae de datos 
            
            messages.success(request, f'Se creo el perfil {new_profile.name}')
            
            
            #bitacora
            Bitacora.objects.create(
                movimiento=f"se creo el perfil: {new_profile.name} con phone {new_profile.phone}"
            )
        return redirect('profile')
    
    else:
        print('No se aguardaron los datos en la bd')
        
        context = {
            'profile':profile
        }
        
        
    return render(request, 'profile.html', context)


def edit_profile(request, profile_id):
    # Obtener el perfil o mostrar 404 si no existe
    profile = get_object_or_404(Profile, pk=profile_id)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            update_profile = form.save(commit=False)
            update_profile.save()
            
            # Registrar en bitácora
            Bitacora.objects.create(
                movimiento=f"Se actualizó el perfil: {update_profile.name} con teléfono {update_profile.phone}"
            )
            
            messages.success(request, 'Perfil actualizado correctamente')
            return redirect('profile')  # Asegúrate que 'profile' es el nombre correcto de tu URL
        
        # Si el formulario no es válido, mostrar errores
        messages.error(request, 'Por favor corrige los errores en el formulario')
        print('No se actualizó el perfil - Errores en el formulario')
    else:
        # Método GET - Mostrar formulario con datos actuales
        form = ProfileForm(instance=profile)
    
    # Contexto para la plantilla (tanto para GET como POST con errores)
    context = {
        'form': form,
        'profile': profile
    }
    
    return render(request, 'edit-profile.html', context)

def delete_profile(request, profile_id):
    # Obtener el perfil o mostrar 404 si no existe
    profile = get_object_or_404(Profile, pk=profile_id)
    profile.estatus = False
    profile.save()
    
    # Guardar información para la bitácora antes de eliminar
    profile_name = profile.name
    profile_phone = profile.phone
    
    # Eliminar el perfil
    #profile.delete()
    
    # Registrar en bitácora
    Bitacora.objects.create(
        movimiento=f"Se borró el perfil: {profile_name} con teléfono {profile_phone}"
    )
    
    return redirect('bitacora')

def delete_bitacora(request, bitacora_id):
    try:
        # Obtener la bitácora o mostrar 404 si no existe
        bitacora = get_object_or_404(Bitacora, pk=bitacora_id)
        
        # Guardar información para la bitácora antes de eliminar
        bitacora_movimiento = bitacora.movimiento
        bitacora_fecha = bitacora.fecha
        
        # Eliminar la bitácora
        bitacora.delete()
        
        # Registrar en bitácora la acción de eliminación
        Bitacora.objects.create(
            movimiento=f"Se borró: {bitacora_movimiento} con fecha {bitacora_fecha}",
            # Añade más campos requeridos por tu modelo Bitacora si es necesario
            # usuario=request.user,
            # fecha=timezone.now()
        )
        
        messages.success(request, 'Bitácora eliminada correctamente')
        return redirect('bitacora')
        
    except Exception as e:
        messages.error(request, f'Ocurrió un error al eliminar la bitácora: {str(e)}')
        return redirect('bitacora')



def report(request):
    profiles = Profile.objects.all().order_by('name')
    time = timezone.now().date()
    
    wb = Workbook()
    ws = wb.active
    
    ws.append(['Username','Nombre','Telefono','Correo'])
    
    for profile in profiles:
        ws.append([profile.username, profile.name, profile.phone, profile.email])
        
    response = HttpResponse(content_type='appliaction/ms-excel')
    response['Content-Disposition'] = f'attachement; filename=profiles-{time}.xlsx'
    
    wb.save(response)
    return response
    
#--------------------------------------------------------------------------------
def sign_in(request):
    if request.method == 'GET':
        return render(request, 'sign-in.html')
    else:
        # Eliminé las comas al final de estas líneas que convertían las variables en tuplas
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is None:
            Bitacora.objects.create(
                user=None,
                movimiento=f"Intento fallido para el usuario: {username}"
            )
            
            return render(request, 'sign-in.html', {
                'error_match': 'Usuario o contraseña incorrectos'  # Corregí "incorectos" a "incorrectos"
            })
        else:
            Bitacora.objects.create(
                user=user,
                movimiento=f"Sesión iniciada: {username}"  # Corregí "sesion" a "Sesión"
            )
            login(request, user)
            return redirect('profile')
            
    
    
    

def sign_up(request):
    if request.method == 'GET':
        return render(request, 'sign-up.html',{
            'form': UserCreationForm()  # Corregido 'from' a 'form' y añadido ()
        })
    else:
        print(request.POST)
        #comparacion de contraseñas
        if request.POST['password1'] == request.POST['password2']:
            #Generar usuario
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1']) 
                
                user.save()
                login(request, user)
                
                
            
                Bitacora.objects.create(
                    user=user,
                    movimiento=f"Registro exitoso: {user.username}"  # Corregido "existoso" a "exitoso"
                )
                return redirect('profile')
                
            except:
                Bitacora.objects.create(
                    user=None,
                    movimiento=f"Intento fallido: {request.POST['username']}"
                )
                return render(request, 'sign-up.html', {  # Corregido sintaxis de llaves
                    'form': UserCreationForm(),
                    'error_exists': "Usuario ya existe"  # Mensaje más genérico
                })
                
                
        else:
            Bitacora.objects.create(
                    user=None,
                    movimiento=f"Registro fallido: {request.POST['username']}"
                )
            
            return render(request, 'sign-up.html', {
                'form': UserCreationForm(),
                'error_match': "Las contraseñas no coinciden"
            })
               
def close(request):
        if request.user.is_authenticated:
            username = request.user.username
        
        Bitacora.objects.create(
                 user=user,
            movimiento=f"Cierra sesion: {username}"  # Corregido "existoso" a "exitoso"
        )
        
        logout(request)
        return redirect('signin')            

        
                
                
                
    
