from django.urls import path
from .views import index, formulario, editar_datos, sesion, terror, accion, aventura, carreras, supervivencia, compra, listado_juegos, crear_juego, juegos_show, detalle_juego,  eliminar_juego, juegos_editar, logout_view, recuperar_contrasenna
urlpatterns = [
    path('princjuegos', index, name='index'),
    path('princjuegos/juegosterror', terror, name="terror"),
    path('princjuegos/juegosaventura', aventura, name="aventura"),
    path('princjuegos/juegosaccion', accion, name="accion"),
    path('princjuegos/juegoscarreras', carreras, name="carreras"),
    path('princjuegos/juegossupervivencia', supervivencia, name="supervivencia"),
    path('princjuegos/juegoscompra', compra, name="compra"),
    path('princjuegos/listado_juegos', listado_juegos, name="listado_juegos"),
    path('princjuegos/crearjuego', crear_juego, name="crear_juego"),
    path('princjuegos/<int:id>/editarjuego', juegos_editar, name="juegos_editar"),
    path('princjuegos/<int:id>/juego_show', juegos_show, name="juegos_show"),
    path('princjuegos/<int:id>/detalle_juego', detalle_juego, name="detalle_juego"),
    path('princjuegos/<int:id>/eliminar_juego', eliminar_juego, name="eliminar_juego"),
    
    path('princjuegos/formulario', formulario, name="formulario"),
    path('princjuegos/editar_datos', editar_datos, name="editar_datos"),
    path('princjuegos/juegossesion', sesion, name="sesion"),
    path('princjuegos/recuperar_contrasenna', recuperar_contrasenna, name="recuperar_contrasenna"),
    path('logout', logout_view, name="logout")

]