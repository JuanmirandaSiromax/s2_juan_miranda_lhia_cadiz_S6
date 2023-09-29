from django.shortcuts import render, get_object_or_404, redirect
from .models import Juego, Categoria , UserProfile
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import role_requiered
from django.contrib.auth.models import User

# Create your views here.



# definicion sesion de usuarios y perfil
def index(request):

    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        clave = request.POST.get('pass')

        user = authenticate(request, username = usuario, password = clave)
        if user is not None:
            # Autenticación exitosa
            login(request, user)
            try:
                profile = user.userprofile  # Obtén el perfil de usuario
                request.session['perfil'] = profile.role
            except UserProfile.DoesNotExist:
                # Si el perfil de usuario no existe, puedes manejarlo aquí
                messages.error(request, 'El perfil de usuario no está configurado correctamente.')
                return redirect('principal')
            
            return redirect('listado_juegos')
        else:
            context = {
                'error': 'Error, inténtelo nuevamente'
            }
            return render(request, 'auth/index.html', context)

    return render(request, 'auth/index.html')

    
@login_required
def listado_usuarios(request):

    user = User.objects.all()
    

    return render(request, 'auth/listado_usuarios.html', {'user': user})
    

def formulario(request):

    if request.method == 'POST':
        first_name = request.POST['first_name']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
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
        
        if password != password2:
            messages.error(request, 'La contraseña debe ser iguales')
            return redirect('formulario')
        
        user = User.objects.create(
            first_name=first_name,
            username=username,
            password=password,
            email=email
            )
        role = 'cliente'
        UserProfile.objects.create(user=user, role=role)

        authenticated_user = authenticate(request, username=username, password=password)
        if authenticated_user:
            login(request, authenticated_user)

        messages.success(request, 'Se ha creado la cuenta correctamente como cliente')

        return redirect('listado_usuarios')
        
    else:
        return render(request, 'auth/formulario.html')  
    
@role_requiered('admin')
def editar_datos(request,id):
    
        usuario = get_object_or_404(User, id=id)
        
        if request.method == 'POST':
            first_name = request.POST['first_name']
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            role = request.POST['role'] 

            usuario.first_name = first_name
            usuario.username = username
            usuario.set_password(password)
            usuario.email = email
            usuario.userprofile.role = role
            usuario.userprofile.save()  
            usuario.save()

            messages.success(request, 'Usuario editado exitosamente.')
            return redirect('listado_usuarios')
        return render(request, 'auth/editar_datos.html', {'usuario': usuario})


@role_requiered('admin','cliente')
def recuperar_contrasenna(request):

    return render(request, 'auth/recuperar_contrasenna.html')
@role_requiered('admin')
def eliminar_usuario(request, id):
    usuario = get_object_or_404(User, id=id)
    usuario.delete()
    messages.success(request, 'Se ha Eliminado Correctamente')
    return redirect('listado_usuarios')
@role_requiered('admin','cliente')
def logout_view (request):
    logout(request)
    return render(request, 'auth/index.html')

# definiciones para juegos 
@login_required
def principal(request):
    return render(request, 'juegos/principal.html')
@login_required
def accion(request):
        
    juegos_accion = Juego.objects.filter(categoria__nombre='ACCION')
   
    return render(request, 'juegos/accion.html',{'juegos_accion': juegos_accion})
@login_required
def supervivencia(request):

    juegos_supervivencia = Juego.objects.filter(categoria__nombre='SUPERVIVENCIA')

    return render(request, 'juegos/supervivencia.html',{'juegos_supervivencia': juegos_supervivencia})
@login_required
def terror(request):

    juegos_terror = Juego.objects.filter(categoria__nombre='TERROR')

    return render(request, 'juegos/terror.html',{'juegos_terror' : juegos_terror})
@login_required
def aventura(request):

    juegos_aventura = Juego.objects.filter(categoria__nombre='AVENTURA')

    return render(request, 'juegos/aventura.html',{'juegos_aventura': juegos_aventura})
@login_required
def carreras(request):

    juegos_carreras = Juego.objects.filter(categoria__nombre='CARRERAS')

    return render(request, 'juegos/carreras.html',{'juegos_carreras': juegos_carreras})

@login_required
def compra(request):
    return render(request, 'juegos/carrito.html')
@login_required
def juegos_show(request, id):
    juego = get_object_or_404(Juego, id=id)
    context = {
        'juego' : juego
         }

    return render(request, 'juegos/juegos_show.html',context)
@login_required
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
        juego.codigo= request.POST['codigo']
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


    return render(request, 'juegos/detalle_juego.html')
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
            codigo=codigo,
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