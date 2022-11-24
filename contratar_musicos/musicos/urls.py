from django.urls import include, path
from django.contrib import admin
from contratar_musicos.musicos import views
app_name = 'musicos'

urlpatterns = [
    path('', views.index, name='index'),
    path('perfil/<slug:slug_musico>', views.perfil_musico, name='perfil_musico'),
    path('unetenos/', views.registro_usuario_musico, name='registro_usuario_musico'),
    path('completar-registro/', views.registro_musico, name='completar_registro_musico'),
    path('categoria/<slug:slug_tipo_musico>', views.tipo_musico, name='tipo_musico'),
    path('registro/visita/', views.registro_visitas, name='registro_visitas'),
    path('obtener/musico/tipo', views.obtener_musicos_tipo, name='obtener_musicos_tipo'),
]
