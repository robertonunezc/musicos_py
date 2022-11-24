from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from contratar_musicos.musicos.models import *
from contratar_musicos.musicos.forms import *
from django.http import HttpResponseRedirect, HttpResponse
from contratar_musicos.musicos.serializer import *
import json


# @login_required
def index(request):
    estado = Estado.objects.get(nombre="Queretaro")
    musicos = Musico.objects.filter(localizacion__estado=estado).order_by('-id')[:8]
    tipos_musicos = TipoMusico.objects.all()
    servicios = Servicios.objects.all()
    tipo_cobro = TipoCobro.objects.all()

    if request.method == 'POST':
        kwargs = {}

        if request.POST.get('nombre') is not "":
            kwargs['nombre__icontains'] = request.POST.get('nombre')

        if request.POST.get('tipo-musico') != "-1":
            tipo_musico_buscar = TipoMusico.objects.get(pk=request.POST.get('tipo-musico'))
            kwargs['tipo_musico'] = tipo_musico_buscar

        if request.POST.get('servicio') != "-1":
            servicios_buscar = Servicios.objects.get(pk=request.POST.get('servicio'))
            kwargs['servicio_musica'] = servicios_buscar

        if request.POST.get('precio-min') is not "" and request.POST.get('precio-max') is not "" and request.POST.get('tipo_cobro') != "-1":
            tipo_cobro_buscar = TipoCobro.objects.get(pk=request.POST.get('tipo_cobro'))
            precio_min_buscar = Precio.objects.filter(valor_minimo__lte=request.POST.get('precio-min'), valor_maximo__gte=request.POST.get('precio-max'), tipo_cobro=tipo_cobro_buscar)
            kwargs['precio__in'] = precio_min_buscar

        if request.POST.get('precio-min') is not "" and request.POST.get('precio-max') is not "" and request.POST.get('tipo_cobro') == "-1":
            precio_min_buscar = Precio.objects.filter(valor_minimo__lte=request.POST.get('precio-min'), valor_maximo__gte=request.POST.get('precio-max'))
            kwargs['precio__in'] = precio_min_buscar

        resultado_busqueda = Musico.objects.filter(**kwargs)
        context = {'resultado_busqueda': resultado_busqueda}
        return render(request, 'musicos/resultado_busqueda.html', context=context)


    context = {
        'musicos': musicos,
        'tipos_musicos': tipos_musicos,
        'servicios': servicios,
        'tipo_cobro': tipo_cobro
    }
    return render(request, 'musicos/index.html', context)


def registro_visitas(request):
    id_musico = request.GET.get('musico')
    try:
        musico = Musico.objects.get(slug=id_musico)
        cantidad_visita = musico.cantidad_visitas + 1
        musico.cantidad_visitas = cantidad_visita
        musico.save()
        json_data = {'rc': 0, 'msg': 'Exito'}

    except Musico.DoesNotExist:
        json_data = {'rc': -1, 'msg': 'Los datos que intenta ver no existen. Lo sentimos'}

    return HttpResponse(json.dumps(json_data), content_type='application/json')


def tipo_musico(request, slug_tipo_musico):
    tipo = TipoMusico.objects.get(slug=slug_tipo_musico)
    musicos = Musico.objects.filter(tipo_musico=tipo)
    context = {'musicos':musicos, 'tipo_musico': tipo}

    return render(request, 'musicos/tipos_musico.html', context=context)


def perfil_musico(request, slug_musico):
    try:
        musico = Musico.objects.get(slug=slug_musico)
        for imagen in musico.imagenes_galeria.all():
            print(imagen.image.url)
    except Musico.DoesNotExist:
        musico = None
    return render(request, 'musicos/perfil_musico.html', {'musico': musico})


def registro_musico(request):
    form = RegistroMusicoForm()
    if request.method == 'POST':
        form = RegistroMusicoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')

    return render(request, 'musicos/registro_musico.html', {'form': form })


def registro_usuario_musico(request):
    form = UsuarioForm()
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        # form.username = form.email
        if form.is_valid():
            usuario = form.save()
            request.session.pop('registered_user', usuario.pk)
            musico_form = RegistroMusicoForm()
            return render(request, 'musicos/registro_musico.html', {'form': musico_form})

    return render(request, 'musicos/registro_usuario_musico.html', {'form': form})


def obtener_musicos_tipo(request):
    slug_tipo_musico = request.GET['tipo_musico']
    tipo = TipoMusico.objects.get(slug=slug_tipo_musico)
    musicos = Musico.objects.filter(tipo_musico=tipo)
    serial = MusicoSerializer(musicos, many=True)
    json_data = {
        'msg': 'Ok',
        'rc': '0',
        'data': serial.data
    }
    return HttpResponse(json.dumps(json_data),content_type='application/json')