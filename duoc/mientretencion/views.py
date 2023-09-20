from django.shortcuts import render, get_object_or_404, redirect
from .models import Juego, Categoria , UserProfile
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import role_requiered
from django.contrib.auth.models import User

# Create your views here.

def index(request):
    return render(request, 'juegos/index.html')


def accion(request):
    return render(request, 'juegos/accion.html')

def supervivencia(request):
    return render(request, 'juegos/supervivencia.html')

def terror(request):
    return render(request, 'juegos/terror.html')

def aventura(request):
    return render(request, 'juegos/aventura.html')

def carreras(request):
    return render(request, 'juegos/carreras.html')

def sesion(request):

    if request.method == 'POST':
        usuario= request.POST.get('usuario')
        clave= request.POST.get('pass')

        user = authenticate (request, username=usuario, password=clave)

        if user is not None:

            profile = UserProfile.objects.get(user=user)

            request.session['perfil'] = profile.role

            login(request, user)
            return redirect('listado_juegos')
        else:
            context ={
                'error' : 'Error intente nuevamente'
            }
            return render(request, 'auth/inicio_sesion.html',context)

    return render(request, 'auth/inicio_sesion.html')


def formulario(request):

    if request.method == 'POST':
        first_name = request.POST['first_name']
        username = request.POST['username']
        password = request.POST['password']
        last_name = request.POST['last_name']
        email = request.POST['email']
        # Validar los datos ingresados 
        if not username:
            messages.error(request, 'Nombre de usuario es obligatorio')
            return redirect('formulario')
        
        if len(password) < 6 or len(password) > 16:
            messages.error(request, 'La contraseña debe tener entre 6 y 16 caracteres')
            return redirect('formulario')
        
        if not any(char.isupper() for char in password):
            messages.error(request, 'La contraseña debe contener al menos una letra mayúscula')
            return redirect('formulario')

        # Verificar si el nombre de usuario ya existe
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso')
            return redirect('formulario')
        
        if password != last_name:
            messages.error(request, 'La contraseña debe ser iguales')
            return redirect('formulario')
        
        User.objects.create(
            first_name=first_name,
            username=username,
            password=password,
            last_name=last_name,
            email=email
            )
        messages.success(request, 'Se ha creado Correctamente')
        return redirect('formulario')
        
    else:
        return render(request, 'auth/formulario.html')  
@login_required
def editar_datos(request):
    user = request.user
    
    if request.method =='POST':
 

        first_name = request.POST[' first_name ']
        username = request.POST[' username ']
        password= request.POST['password']
        last_name = request.POST['last_name']
        email = email
        
        user.first_name = first_name
        user.username = username
        user.set_password(password)
        user.last_name = last_name
        user.email = email

        user.save()
        messages.success(request, 'Se ha Actualizado Correctamente') 
        return redirect('formulario') 
    return render(request, 'auth/editar_datos.html', {'user': user})

@role_requiered('admin','cliente')
def recuperar_contrasenna(request):

    return render(request, 'auth/recuperar_contrasenna.html')

@role_requiered('admin','cliente')
def logout_view (request):
    logout(request)
    return render(request, 'auth/inicio_sesion.html')


@role_requiered('admin','cliente')
def compra(request):
    return render(request, 'juegos/carrito.html')
@role_requiered('admin','cliente')
def juegos_show(request, id):
    juego = get_object_or_404(Juego, id=id)
    context = {
        'juego' : juego
         }

    return render(request, 'juegos/juegos_show.html',context)


@role_requiered('admin','cliente')
def listado_juegos (request):
    juegos = Juego.objects.all()

    perfil = request.session.get('perfil')

    context ={
        'juegos' : juegos,
        'perfil' : perfil
    }
    return render (request, 'juegos/listado_juegos.html',context)
@role_requiered('admin')
def juegos_editar(request,id):
    juego = get_object_or_404(Juego, id=id)
    
    if request.method =='POST':
        categoria_id = request.POST.get ('categoria')
        categoria = get_object_or_404(Categoria, id=categoria_id)    

        juego.nombre = request.POST['nombre']
        juego.codigo_isbn = request.POST['codigo']
        juego.descripcion = request.POST['descripcion']
        juego.categoria = categoria

        if 'imagen' in request.FILES:
            juego.imagen = request.FILES['imagen']
        
        juego.save()
        messages.success(request, 'Se ha Actualizado Correctamente')

    
    categorias =Categoria.objects.all()
    context ={
        'juego' : juego,
        'categorias' : categorias
    }
    return render(request, 'juegos/juegos_editar.html', context)
@role_requiered('admin','cliente')
def detalle_juego(request,id):

    juego =get_object_or_404(Juego, id=id)
    context ={
        'juego' : juego
    }
    return render(request, 'juegos/detalle_juego.html',context)
@role_requiered('admin')
def crear_juego (request): 

    if request.method =='POST':
        categoria_id = request.POST.get ('categoria')
        categoria = get_object_or_404(Categoria, id=categoria_id)

        codigo = request.POST.get('codigo')
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        imagen = request.FILES.get('imagen')

        Juego.objects.create(
            codigo_isbn=codigo,
            nombre=nombre,
            descripcion=descripcion,
            imagen=imagen,
            categoria=categoria
            )
        messages.success(request, 'Se ha creado Correctamente')
        return redirect('listado_juegos')

    categorias = Categoria.objects.all()
    
    contexto = {
        'categorias': categorias
    }
    
    return render (request, 'juegos/crearjuego.html',contexto)
@role_requiered('admin')
def eliminar_juego (request, id):
    juego = get_object_or_404(Juego, id=id)
    juego.delete()
    messages.success(request, 'Se ha Eliminado Correctamente')
    return redirect('listado_juegos')