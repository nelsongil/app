import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import IntegrityError
from django.core.paginator import Paginator
from django.http import Http404
from datetime import datetime, date, time, timedelta
from django.db import transaction

from .forms import ClienteForm, ObrasForm, FiltroForm, MaterialesfForm, MaterialesForm, UsuarioNuevoForm, UsuarioEditarForm
from .models import Clientes, Obras, MaterialesF, Materiales, Horas

import json
import calendar

def is_superuser(user):
    return user.is_superuser


@login_required
@user_passes_test(is_superuser, login_url='home2')
def home(request):
    return render(request, 'home.html')


def botones_activos(tipo):
    #print("Función Botones Activos")
    match tipo:
        case 'J0':
            # Jornada Iniciada
            botones_habilitados = {
                'J0': True,  # Jornada Laboral Inicio
                'J1': False,  # Jornada Laboral Final
                'B0': False,  # Bocadillo Inicio
                'B1': True,  # Bocadillo Final
                'S0': False,  # Salida en Horario Laboral Inicio
                'S1': True,  # Salida en Horario Laboral Final
            }
            #("BA_home 1: " + tipo)

        case 'J1':
            # Jornada Finalizada
            botones_habilitados = {
                'J0': True,  # Jornada Laboral Inicio
                'J1': True,  # Jornada Laboral Final
                'B0': True,  # Bocadillo Inicio
                'B1': True,  # Bocadillo Final
                'S0': True,  # Salida en Horario Laboral Inicio
                'S1': True,  # Salida en Horario Laboral Final
            }
            #print("BA_home 2: " + tipo)
        case 'B0':
            # Bocadillo Iniciado
            botones_habilitados = {
                'J0': True,  # Jornada Laboral Inicio
                'J1': True,  # Jornada Laboral Final
                'B0': True,  # Bocadillo Inicio
                'B1': False,  # Bocadillo Final
                'S0': True,  # Salida en Horario Laboral Inicio
                'S1': True,  # Salida en Horario Laboral Final
            }
            #print("BA_home 3: " + tipo)
        case 'B1':
            # Bocadillo Finalizado
            botones_habilitados = {
                'J0': True,  # Jornada Laboral Inicio
                'J1': False,  # Jornada Laboral Final
                'B0': True,  # Bocadillo Inicio
                'B1': True,  # Bocadillo Final
                'S0': False,  # Salida en Horario Laboral Inicio
                'S1': True,  # Salida en Horario Laboral Final
            }
            #print("BA_home 4: " + tipo)
        case 'S0':
            # Salida Extra
            botones_habilitados = {
                'J0': True,  # Jornada Laboral Inicio
                'J1': True,  # Jornada Laboral Final
                'B0': True,  # Bocadillo Inicio
                'B1': True,  # Bocadillo Final
                'S0': True,  # Salida en Horario Laboral Inicio
                'S1': False,  # Salida en Horario Laboral Final
            }
            #print("BA_home 5: " + tipo)
        case 'S1':
            # Entrada Extra
            botones_habilitados = {
                'J0': True,  # Jornada Laboral Inicio
                'J1': False,  # Jornada Laboral Final
                'B0': False,  # Bocadillo Inicio
                'B1': True,  # Bocadillo Final
                'S0': False,  # Salida en Horario Laboral Inicio
                'S1': True,  # Salida en Horario Laboral Final
            }
            #print("BA_home 6: " + tipo)

        case 'J00':
            # Nuevo Registro
            botones_habilitados = {
                'J0': False,  # Jornada Laboral Inicio
                'J1': True,  # Jornada Laboral Final
                'B0': True,  # Bocadillo Inicio
                'B1': True,  # Bocadillo Final
                'S0': True,  # Salida en Horario Laboral Inicio
                'S1': True,  # Salida en Horario Laboral Final
            }

            #print("BA_home 7: " + tipo)

        case _:
            # Error
            botones_habilitados = {
                'J0': False,  # Jornada Laboral Inicio
                'J1': True,  # Jornada Laboral Final
                'B0': True,  # Bocadillo Inicio
                'B1': True,  # Bocadillo Final
                'S0': True,  # Salida en Horario Laboral Inicio
                'S1': True,  # Salida en Horario Laboral Final
            }
            #print("BA_home 8: " + tipo)

    # Cara del botón

    if botones_habilitados['J0']:
        botones_habilitados['J0B'] = "btn btn-outline-primary btn-m col"
    else:
        botones_habilitados['J0B'] = "btn btn-primary btn-m col"

    if botones_habilitados['J1']:
        botones_habilitados['J1B'] = "btn btn-outline-primary btn-m col"
    else:
        botones_habilitados['J1B'] = "btn btn-primary btn-m col"

    if botones_habilitados['B0']:
        botones_habilitados['B0B'] = "btn btn-outline-success btn-m col"
    else:
        botones_habilitados['B0B'] = "btn btn-success btn-m col"

    if botones_habilitados['B1']:
        botones_habilitados['B1B'] = "btn btn-outline-success btn-m col"
    else:
        botones_habilitados['B1B'] = "btn btn-success btn-m col"

    if botones_habilitados['S0']:
        botones_habilitados['S0B'] = "btn btn-outline-warning btn-m col"
    else:
        botones_habilitados['S0B'] = "btn btn-warning btn-m col"

    if botones_habilitados['S1']:
        botones_habilitados['S1B'] = "btn btn-outline-warning btn-m col"
    else:
        botones_habilitados['S1B'] = "btn btn-warning btn-m col"

    #print("BA Tipo: " + tipo)
    #print("BA Botones: " + str(botones_habilitados))

    return (botones_habilitados)


def cerrar_registro(usuario):
    # Obtener el último horario del usuario
    ultimo_horario = Horas.objects.filter(
        idUsuario=usuario.id).order_by('-id').first()

    if ultimo_horario:
        fecha_concreta = ultimo_horario.fecha
        with transaction.atomic():
            # Verificar si existen registros J0 sin J1
            j0_registros = Horas.objects.filter(
                idUsuario=usuario, fecha=fecha_concreta, tipo='J0')
            j1_registros = Horas.objects.filter(
                idUsuario=usuario, fecha=fecha_concreta, tipo='J1')
            # Verificar si existen registros B0 sin B1
            b0_registros = Horas.objects.filter(
                idUsuario=usuario, fecha=fecha_concreta, tipo='B0')
            b1_registros = Horas.objects.filter(
                idUsuario=usuario, fecha=fecha_concreta, tipo='B1')
            # Verificar si existen registros B0 sin B1
            s0_registros = Horas.objects.filter(
                idUsuario=usuario, fecha=fecha_concreta, tipo='S0')
            s1_registros = Horas.objects.filter(
                idUsuario=usuario, fecha=fecha_concreta, tipo='S1')

            if j0_registros.count() > j1_registros.count():
                # No se cerro la jornada, crea el registro J1
                cerrar_jornada = Horas(
                    fecha=fecha_concreta,
                    hora=time(16, 0),
                    tipo='J1',
                    idUsuario=usuario,
                    latitud=0,
                    longitud=0,
                )
                cerrar_jornada.save()

            if b0_registros.count() > b1_registros.count():
                # No se cerro el bocadillo, crea el registro B1
                cerrar_bocadillo = Horas(
                    fecha=fecha_concreta,
                    hora=time(16, 0),
                    tipo='B1',
                    idUsuario=usuario,
                    latitud=0,
                    longitud=0,
                )
                cerrar_bocadillo.save()

            if s0_registros.count() > s1_registros.count():
                # No se cerro la salida, crea el registro S1
                cerrar_salida = Horas(
                    fecha=fecha_concreta,
                    hora=time(16, 0),
                    tipo='S1',
                    idUsuario=usuario,
                    latitud=0,
                    longitud=0,
                )
                cerrar_salida.save()

    else:
        # Manejar el caso en el que no hay horarios para el usuario
        # Puedes registrar un mensaje de error o tomar otras medidas adecuadas.
        pass


@login_required
def home2(request):
    entorno = {}
    usuario = request.user
    ultimo_horario = Horas.objects.filter(
        idUsuario=usuario.id).order_by('-id').first()
    robohash = ('https://robohash.org/usuario' +
                str(usuario.id))
    entorno['usuario'] = usuario
    entorno['robohash'] = robohash
    hoy = date.today()

    # Hay registros
    # Determinar si existen registros de 'B1' o 'J1' para la fecha actual
    registros_bocadillo = Horas.objects.filter(
        idUsuario=usuario.id, tipo='B1', fecha=hoy).exists()
    registros_jornada_finalizada = Horas.objects.filter(
        idUsuario=usuario.id, tipo='J1', fecha=hoy).exists()

    # Habilitar o deshabilitar botones en función de los registros
    if registros_jornada_finalizada:
        entorno['botones_habilitados'] = botones_activos("J1")
    elif registros_bocadillo:
        entorno['botones_habilitados'] = botones_activos("B1")

        # Deshabilitar los botones 'B0' y 'B1' cuando existe un registro de 'B1'
        entorno['botones_habilitados']['B0'] = True
        entorno['botones_habilitados']['B1'] = True
    else:
        # Otros casos como 'J0', 'B0', 'S0', 'S1', 'J00', o casos de error
        if ultimo_horario is not None:
            # Es el último registro de hoy?
            if ultimo_horario.fecha == date.today():
                entorno['botones_habilitados'] = botones_activos(
                    ultimo_horario.tipo)
            else:
                if ultimo_horario.tipo != "J1":
                    # Jornada no cerrada
                    cerrar_registro(usuario)
                    entorno['botones_habilitados'] = botones_activos("J00")
                else:
                    # Nuevo Registro
                    entorno['botones_habilitados'] = botones_activos("J00")
        else:
            # Nuevo Registro
            entorno['botones_habilitados'] = botones_activos("J00")

    return render(request, 'home2.html', {'entorno': entorno})


def pruebas(request):

    return render(request)


def obtener_direccion_desde_coordenadas(latitud, longitud):
    # Construye la URL para la solicitud de geocodificación en Nominatim
    url = f'https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat={latitud}&lon={longitud}'

    try:
        # Realiza la solicitud a la API de Nominatim
        response = requests.get(url)
        data = response.json()
        # Verifica si la solicitud fue exitosa y obtiene la dirección si está disponible
        if 'display_name' in data:
            # address = data['display_name']
            calle = data['address']['road']
            residencial = data['address']['residential']
            ciudad = data['address']['town']
            provincia = data['address']['state_district']
            address = calle + ", " + residencial + ", " + ciudad + ", " + provincia
        else:
            address = 'No se pudo encontrar la dirección.'

        return address

    except Exception as e:
        return 'Error al obtener la dirección: ' + str(e)


@login_required
def marcar_tarjeta(request):

    usuario = request.user
    boton_id = request.POST.get("boton_id")
    longitud = request.POST.get("longitud", 0)
    latitud = request.POST.get("latitud", 0)

    robohash = ('https://robohash.org/usuario' + str(usuario.id))
    entorno = {'robohash': robohash}

    #print("Usuario: " + str(usuario.id))
    #print("Boton ID: " + boton_id)
    #print("Latitud: " + latitud)
    #print("Longitud: " + longitud)

    ultimo_horario = Horas.objects.filter(
        idUsuario=usuario).order_by('-id').first()
    # Determinar si existen registros de 'B1' o 'J1' para la fecha actual
    hoy = date.today()
    registros_bocadillo = Horas.objects.filter(
        idUsuario=usuario.id, tipo='B1', fecha=hoy).exists()
    entorno = {'robohash': robohash, 'botones_habilitados': {}}

    if ultimo_horario is not None:
        match boton_id:
            case 'J0':
                # Jornada Iniciada
                nueva_salida = Horas(
                    fecha=datetime.now().date(),
                    hora=datetime.now().time(),
                    tipo=boton_id,
                    idUsuario=usuario,
                    latitud=latitud,
                    longitud=longitud,
                )
                nueva_salida.save()
                entorno['mensaje'] = 'Se ha registrado la entrada correctamente.'

                #print("MT_home 1: " + boton_id)

            case 'J1':
                # Jornada Finalizada
                nueva_salida = Horas(
                    fecha=datetime.now().date(),
                    hora=datetime.now().time(),
                    tipo=boton_id,
                    idUsuario=usuario,
                    latitud=latitud,
                    longitud=longitud,
                )
                nueva_salida.save()
                entorno['mensaje'] = 'Se ha registrado la salida correctamente.'

                #print("MT_home 2: " + boton_id)
            case 'B0':
                # Bocadillo Iniciado
                nueva_salida = Horas(
                    fecha=datetime.now().date(),
                    hora=datetime.now().time(),
                    tipo=boton_id,
                    idUsuario=usuario,
                    latitud=latitud,
                    longitud=longitud,
                )
                nueva_salida.save()
                entorno['mensaje'] = 'Ha comenzado el bocadillo.'

                #print("MT_home 3: " + boton_id)
            case 'B1':
                # Bocadillo Finalizado
                nueva_salida = Horas(
                    fecha=datetime.now().date(),
                    hora=datetime.now().time(),
                    tipo=boton_id,
                    idUsuario=usuario,
                    latitud=latitud,
                    longitud=longitud,
                )
                nueva_salida.save()
                entorno['mensaje'] = 'Ha finalizado el bocadillo.'

                #print("MT_home 4: " + boton_id)
            case 'S0':
                # Salida Extra
                nueva_salida = Horas(
                    fecha=datetime.now().date(),
                    hora=datetime.now().time(),
                    tipo=boton_id,
                    idUsuario=usuario,
                    latitud=latitud,
                    longitud=longitud,
                )
                nueva_salida.save()
                entorno['mensaje'] = 'Se ha registrado una salida extraordinaria.'

                #print("MT_home 5: " + boton_id)
            case 'S1':
                # Entrada Extra
                nueva_salida = Horas(
                    fecha=datetime.now().date(),
                    hora=datetime.now().time(),
                    tipo=boton_id,
                    idUsuario=usuario,
                    latitud=latitud,
                    longitud=longitud,
                )
                nueva_salida.save()
                entorno['mensaje'] = 'Se ha registrado una entrada extraordinaria.'
                #print("MT_home 6: " + boton_id)

            case 'J00':
                # Jornada NO finalizada
                nueva_salida = Horas(
                    fecha=datetime.now().date(),
                    hora=datetime.now().time(),
                    tipo='J00',
                    idUsuario=usuario,
                    latitud=latitud,
                    longitud=longitud,
                )
                nueva_salida.save()
                entorno['mensaje'] = 'Se cerró el último día que quedó abierto.'

                #print("MT_home 7: " + boton_id)

            case _:
                # Error
                entorno['mensaje'] = 'Ocurrio un error durante el proceso.'
                #print("MT_home 8: " + boton_id)
    else:
        nueva_salida = Horas(
            fecha=datetime.now().date(),
            hora=datetime.now().time(),
            tipo=boton_id,
            idUsuario=usuario,
            latitud=latitud,
            longitud=longitud,
        )
        nueva_salida.save()
        #print("Se ha registrado la entrada")

    if registros_bocadillo:

        # Deshabilitar los botones 'B0' y 'B1' cuando existe un registro de 'B1'
        entorno['botones_habilitados']['B0'] = True
        entorno['botones_habilitados']['B1'] = True

    botones_habilitados = botones_activos(nueva_salida.tipo)
    entorno['botones_habilitados'] = botones_habilitados

    return render(request, 'home2.html', {'entorno': entorno})


@login_required
def horas_list(request):
    return render(request, 'usr_horas.html')


@login_required
def horas_informe(request):
    usuario = request.user
    context = {}
    entorno = {}
    mensaje = ""
    fecha0 = ""
    fechaini=""
    fechafin=""
    tipo_div = "div-diario"

    chk_diario = "checked"
    chk_semanal = ""
    chk_mensual = ""
    chk_rango = ""

    if request.method == 'POST':
        periodo_seleccionado = request.POST.get('periodo')
        #print("Informe - Periodo Selecionado " + periodo_seleccionado)
        if periodo_seleccionado == 'diario':
            # Llama a la función de informe diario
            fecha0 = request.POST.get('fecha_picker')
            tipo_div = "div-diario"
            horas_informe_diario(request, context)
        elif periodo_seleccionado == 'semanal':
            # Llama a la función de informe semanal
            fecha0 = request.POST.get('fecha_picker')
            tipo_div = "div-semanal"
            chk_diario = ""
            chk_semanal = "checked"
            chk_mensual = ""
            chk_rango = ""
            context, entorno = horas_informe_semanal(request, context)
        elif periodo_seleccionado == 'mensual':
            # Llama a la función de informe mensual
            fecha0 = request.POST.get('fecha_picker')
            tipo_div = "div-mensual"
            chk_diario = ""
            chk_semanal = ""
            chk_mensual = "checked"
            chk_rango = ""
            context, entorno = horas_informe_mensual(request, context)
        elif periodo_seleccionado == 'rango':
            # Llama a la función de informe por rango
            fechaini = request.POST.get('fecha_inicio')
            fechafin = request.POST.get('fecha_fin')            
            tipo_div = "div-rango"
            chk_diario = ""
            chk_semanal = ""
            chk_mensual = ""
            chk_rango = "checked"
            context, entorno = horas_informe_rango(request, context)
        else:
            # Manejar caso no válido
            fecha0 = request.POST.get('fecha_picker')
            tipo_div = "div-diario"
            chk_diario = "disabled"
            chk_semanal = "disabled"
            chk_mensual = "disabled"
            chk_rango = "disabled"
            mensaje = "Ocurrio un error al selecciónar el filtro. Pongase en contacto con el soporte."


    entorno['usuario'] = usuario
    entorno['robohash'] = ('https://robohash.org/usuario' + repr(usuario.id))
    entorno['mensaje'] = mensaje
    entorno['fecha0'] = fecha0
    entorno['tipo_div'] = tipo_div
    entorno['hoy'] = str(date.today())
    entorno['chk_diario'] = chk_diario
    entorno['chk_semanal'] = chk_semanal
    entorno['chk_mensual'] = chk_mensual
    entorno['chk_rango'] = chk_rango
    entorno['fechaini'] = fechaini
    entorno['fechafin'] = fechafin


    print("Context Función PPAL: " + str(context))
    #print("Entorno Función PPAL: " + str(entorno))
    print("Div a mostrar: " + str(tipo_div))

    return render(request, 'home2_horas.html', {'context': context, 'entorno': entorno})


@login_required
def horas_informe_diario(request, context):
    print("-------------")
    print("informe Diario")
    print("-------------")

    # Informe de Horas Diario
    mensaje = None
    entorno = {}
    fecha_str = None
    diferencia_tiempo = None
    horas_informe_list = []
    diferencia_tiempo = timedelta(hours=0)

    fecha_str = request.POST.get('fecha_picker')

    if fecha_str:
        horas_informe_list = Horas.objects.filter(fecha=fecha_str)

        # Mapeo de tipos a textos
        registro = []
        tipo_texto_mapping = {
            'J0': 'Inicio de Jornada Laboral',
            'J1': 'Fin de Jornada Laboral',
            'B0': 'Inicio Bocadillo',
            'B1': 'Fin Bocadillo',
            'S0': 'Salida motiv. Personales',
            'S1': 'Vuelta motiv. Pesonales',
        }

        for registro in horas_informe_list:
            tipo_texto = tipo_texto_mapping.get(registro.tipo, registro.tipo)
            registro.tipo_texto = tipo_texto
            latitud = registro.latitud
            longitud = registro.longitud
            registro.direccion = obtener_direccion_desde_coordenadas(
                latitud, longitud)

        # Calcular el total de horas de jornada laboral
        total_horas_jornada = 0

        j1 = horas_informe_list.filter(tipo='J1').first()
        j0 = horas_informe_list.filter(tipo='J0').first()

        if j1 and j0:
            hora_inicio = datetime.combine(datetime.now().date(), j0.hora)
            hora_fin = datetime.combine(datetime.now().date(), j1.hora)

            # Verifica si hay un inicio de bocadillo antes de la hora de inicio
            b0 = horas_informe_list.filter(
                tipo='B0').filter(hora__lt=j0.hora).first()
            if b0:
                hora_inicio = datetime.combine(datetime.now().date(), b0.hora)

            # Verifica si hay un fin de bocadillo después de la hora de fin
            b1 = horas_informe_list.filter(
                tipo='B1').filter(hora__gt=j1.hora).first()
            if b1:
                hora_fin = datetime.combine(datetime.now().date(), b1.hora)

            # Calcula la diferencia de tiempo en segundos
            diferencia_tiempo = hora_fin - hora_inicio
            total_horas_jornada = max(
                diferencia_tiempo.total_seconds() / 3600, 0)

        # Calcular el total de horas de bocadillo
        total_horas_bocadillo = 0

        b1 = horas_informe_list.filter(tipo='B1').first()
        b0 = horas_informe_list.filter(tipo='B0').first()

        if b1 and b0:
            hora_inicio_bocadillo = datetime.combine(
                datetime.now().date(), b0.hora)
            hora_fin_bocadillo = datetime.combine(
                datetime.now().date(), b1.hora)
            diferencia_tiempo_bocadillo = hora_fin_bocadillo - hora_inicio_bocadillo
            total_horas_bocadillo = max(
                diferencia_tiempo_bocadillo.total_seconds() / 3600, 0)

            # Ajustar la jornada laboral si el tiempo de bocadillo es menor a 30 minutos
            if total_horas_bocadillo < 0.5:
                diferencia_a_agregar = timedelta(
                    minutes=(30 - total_horas_bocadillo * 60))
                diferencia_tiempo += diferencia_a_agregar
                total_horas_jornada = max(
                    diferencia_tiempo.total_seconds() / 3600, 0)
            else:
                # Restar tiempo de bocadillo si es mayor a 30 minutos
                total_horas_jornada = max(
                    diferencia_tiempo.total_seconds() / 3600 - 0.5, 0)
        else:
            # Si no hay registros de bocadillo, calcular la jornada sin ajustes
            total_horas_jornada = max(
                diferencia_tiempo.total_seconds() / 3600, 0)

        # Calcular el total de horas de salida extraordinaria
        total_horas_salida_extra = 0

        s1_list = horas_informe_list.filter(tipo='S1')
        s0_list = horas_informe_list.filter(tipo='S0')

        for s1, s0 in zip(s1_list, s0_list):
            if s1 and s0:
                # Crear objetos datetime ficticios con la misma fecha
                s1_datetime = datetime.combine(datetime.now().date(), s1.hora)
                s0_datetime = datetime.combine(datetime.now().date(), s0.hora)

                # Calcular la diferencia de tiempo
                diferencia_tiempo = s1_datetime - s0_datetime

                # Calcular las horas en formato decimal
                horas_salida_extra = diferencia_tiempo.total_seconds() / 3600
                total_horas_salida_extra += max(horas_salida_extra, 0)

        # Restar el tiempo de la salida extraordinaria del tiempo de jornada laboral
        total_horas_jornada -= total_horas_salida_extra

        # Formatear los totales en el formato HH:MM:SS con 2 dígitos para los segundos
        total_horas_bocadillo_hhmmss = "{:02d}:{:02d}:{:02d}".format(
            int(total_horas_bocadillo // 1),
            int((total_horas_bocadillo % 1) * 60),
            # Redondea los segundos a 2 dígitos
            int(total_horas_bocadillo % 60)
        )

        if total_horas_jornada > 0:
            total_horas_jornada_hhmmss = "{:02d}:{:02d}:{:02d}".format(
                int(total_horas_jornada // 1),
                int((total_horas_jornada % 1) * 60),
                # Redondea los segundos a 2 dígitos
                int(total_horas_jornada % 60)
            )
        else:
            total_horas_jornada_hhmmss = "-"

        total_horas_salida_extra_hhmmss = "{:02d}:{:02d}:{:02d}".format(
            int(total_horas_salida_extra // 1),
            int((total_horas_salida_extra % 1) * 60),
            # Redondea los segundos a 2 dígitos
            int(total_horas_salida_extra % 60)
        )

        context['horas_informe_list'] = horas_informe_list
        context['total_horas_jornada'] = total_horas_jornada_hhmmss
        context['total_horas_bocadillo'] = total_horas_bocadillo_hhmmss
        context['total_horas_salida_extra'] = total_horas_salida_extra_hhmmss
        mensaje = "Informe Diario " + fecha_str

    else:
        mensaje = "No se encontraron registros"

    entorno['mensaje'] = mensaje
    #print("HI Diario - Contexto: " + str(context))
    #print("HI Diario - Entorno: " + str(entorno))
    return context, entorno


@login_required
def horas_informe_semanal(request, context):
    mensaje = ''
    fecha_str = request.POST.get('fecha_picker')
    fecha_seleccionada = datetime.strptime(fecha_str, '%Y-%m-%d').date()

    inicio_semana = fecha_seleccionada - timedelta(days=fecha_seleccionada.weekday())
    fin_semana = inicio_semana + timedelta(days=6)

    horas_informe_list = []
    total_dias_trabajados = 0  # Contador de días trabajados
    horas_diarias = 8  # Número de horas laborales diarias

    total_horas_jornada_semana = 0
    total_horas_bocadillo_semana = 0
    total_horas_salida_extra_semana = 0
    total_horas_trabajadas_semana = 0

    # Crear un único registro por fecha con valores acumulativos
    for dia in range(7):
        fecha_actual = inicio_semana + timedelta(days=dia)
        registros_dia = Horas.objects.filter(fecha=fecha_actual)

        if registros_dia.exists():
            j0 = registros_dia.filter(tipo='J0').first()
            j1 = registros_dia.filter(tipo='J1').first()
            b0 = registros_dia.filter(tipo='B0').first()
            b1 = registros_dia.filter(tipo='B1').first()
            s0 = registros_dia.filter(tipo='S0').first()
            s1 = registros_dia.filter(tipo='S1').first()

            if j0 and j1:
                j_hora_inicio = datetime.combine(datetime.now().date(), j0.hora)
                j_hora_fin = datetime.combine(datetime.now().date(), j1.hora)
                total_jornada = (j_hora_fin - j_hora_inicio).total_seconds() / 3600
            else:
                total_jornada = 0

            if b0 and b1:
                b_hora_inicio = datetime.combine(datetime.now().date(), b0.hora)
                b_hora_fin = datetime.combine(datetime.now().date(), b1.hora)
                total_bocadillo = (b_hora_fin - b_hora_inicio).total_seconds() / 3600
            else:
                total_bocadillo = 0

            if s0 and s1:
                s_hora_inicio = datetime.combine(datetime.now().date(), s0.hora)
                s_hora_fin = datetime.combine(datetime.now().date(), s1.hora)
                total_salida_extra = (s_hora_fin - s_hora_inicio).total_seconds() / 3600
            else:
                total_salida_extra = 0

            horas_trabajadas = total_jornada - total_salida_extra

            # Calcular bocadillo según reglas
            if total_bocadillo > 0.5:
                horas_trabajadas -= (total_bocadillo - 0.5) 
            elif total_bocadillo < 0.5:
                horas_trabajadas += (0.5 - total_bocadillo) 

            total_jornada_hhmmss = "{:02d}:{:02d}:{:02d}".format(
                int(total_jornada),
                int((total_jornada % 1) * 60),
                int((total_jornada * 3600) % 60)
            )

            total_bocadillo_hhmmss = "{:02d}:{:02d}:{:02d}".format(
                int(total_bocadillo),
                int((total_bocadillo % 1) * 60),
                int((total_bocadillo * 3600) % 60)
            )

            total_salida_extra_hhmmss = "{:02d}:{:02d}:{:02d}".format(
                int(total_salida_extra),
                int((total_salida_extra % 1) * 60),
                int((total_salida_extra * 3600) % 60)
            )
            
            if horas_trabajadas >= horas_diarias:
                eficiencia_laboral_hhmmss= "{:02d}:{:02d}:{:02d}".format(
                    int((horas_trabajadas - horas_diarias) // 1),
                    int(((horas_trabajadas - horas_diarias) % 1) * 60),
                    int(((horas_trabajadas - horas_diarias) * 3600) % 60))
            else:
                eficiencia_laboral_hhmmss= "-{:02d}:{:02d}:{:02d}".format(
                    int((horas_diarias - horas_trabajadas) // 1),
                    int(((horas_diarias - horas_trabajadas) % 1) * 60),
                    int(((horas_diarias - horas_trabajadas) * 3600) % 60))
                
            horas_informe_list.append({
                'fecha': fecha_actual.strftime('%d/%m/%Y'),
                'total_jornada': total_jornada_hhmmss,
                'total_bocadillo': total_bocadillo_hhmmss,
                'total_salida_extra': total_salida_extra_hhmmss,
                'horas_trabajadas': "{:02d}:{:02d}:{:02d}".format(
                    int(horas_trabajadas),
                    int((horas_trabajadas % 1) * 60),
                    int((horas_trabajadas * 3600) % 60)
                ),
                'eficiencia_laboral_hhmmss': eficiencia_laboral_hhmmss
            })

            total_horas_jornada_semana += total_jornada
            total_horas_bocadillo_semana += total_bocadillo
            total_horas_salida_extra_semana += total_salida_extra
            total_horas_trabajadas_semana += horas_trabajadas

            if total_jornada > 0:
                total_dias_trabajados += 1

    # Calcular horas útiles y diferencia
    horas_utiles_semana = total_dias_trabajados * horas_diarias
    if horas_utiles_semana > total_horas_trabajadas_semana:
        diferencia_semana_class = "text_danger"
    else:
        diferencia_semana_class = "text_green"

    diferencia_semana = (horas_utiles_semana * 3600) - total_horas_trabajadas_semana * 3600

    # Formatear los totales semanales
    total_horas_jornada_semana_hhmm = "{:02d}:{:02d}".format(
        int(total_horas_jornada_semana),
        int((total_horas_jornada_semana % 1) * 60)
    )
    total_horas_bocadillo_semana_hhmm = "{:02d}:{:02d}".format(
        int(total_horas_bocadillo_semana),
        int((total_horas_bocadillo_semana % 1) * 60)
    )
    total_horas_salida_extra_semana_hhmm = "{:02d}:{:02d}".format(
        int(total_horas_salida_extra_semana),
        int((total_horas_salida_extra_semana % 1) * 60)
    )
    total_horas_trabajadas_semana_hhmm = "{:02d}:{:02d}".format(
        int(total_horas_trabajadas_semana),
        int((total_horas_trabajadas_semana % 1) * 60)
    )
    diferencia_semana_hhmm = "{:02d}:{:02d}:{:02d}".format(
            int(diferencia_semana // 3600),
            int((diferencia_semana % 3600) // 60),
            int(diferencia_semana % 60)
    )
    horas_utiles_semana_hhmm = "{:02d}:{:02d}".format(
        int(horas_utiles_semana),
        int((horas_utiles_semana % 1) * 60)
    )
    
    # Agregar una lista de días de la semana
    dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']

    # Inicializar una lista vacía para los datos diarios
    datos_diarios = []

    # Crear un diccionario para mapear los nombres de los días a las fechas en 'horas_informe_list'
    dias_a_fechas = {
        'Lunes': inicio_semana,
        'Martes': inicio_semana + timedelta(days=1),
        'Miércoles': inicio_semana + timedelta(days=2),
        'Jueves': inicio_semana + timedelta(days=3),
        'Viernes': inicio_semana + timedelta(days=4),
        'Sábado': inicio_semana + timedelta(days=5),
    }

    for dia in dias_semana:
        fecha_actual = dias_a_fechas[dia]

        # Buscar la entrada correspondiente en 'horas_informe_list' según la fecha
        entrada_dia = next((dia_info for dia_info in horas_informe_list if dia_info['fecha'] == fecha_actual.strftime('%d/%m/%Y')), None)

        if entrada_dia:
            # Si se encuentra una entrada correspondiente en 'horas_informe_list', usa esos datos
            datos_dia = {
                'nombre_dia': dia,
                'datos':[
                    {'tipo': 'horas_trabajadas', 'valor': entrada_dia['total_jornada']},
                    {'tipo': 'bocadillos', 'valor': entrada_dia['total_bocadillo']},
                    {'tipo': 'salidas_extras', 'valor': entrada_dia['total_salida_extra']},
                    {'tipo': 'rendimiento', 'valor': entrada_dia['horas_trabajadas']},
                ]
            }
        else:
            # Si no se encuentra una entrada, usa valores predeterminados o en blanco
            datos_dia = {
                'nombre_dia': dia,
                'datos':[
                    {'tipo': 'horas_trabajadas', 'valor': '00:00:00'},
                    {'tipo': 'bocadillos', 'valor': '00:00:00'},
                    {'tipo': 'salidas_extras', 'valor': '00:00:00'},
                    {'tipo': 'rendimiento', 'valor:': '00:00:00',}
                ]
            }

        datos_diarios.append(datos_dia)

    entorno = {
        'mensaje': mensaje,
        'inicio_semana': inicio_semana.strftime('%d/%m/%Y'),
        'fin_semana': fin_semana.strftime('%d/%m/%Y'),
    }

    #print("Datos Diarios:")
    #for dato in datos_diarios:
    #    print(dato)
    datos_diarios_json = json.dumps(datos_diarios)
    print(datos_diarios_json)
    
    context = {
        'horas_informe_list': horas_informe_list,
        'total_dias_trabajados': total_dias_trabajados,
        'horas_utiles_semana': horas_utiles_semana_hhmm,
        'diferencia_semana': diferencia_semana_hhmm,
        'diferencia_semana_class': diferencia_semana_class,
        'total_horas_jornada_semana': total_horas_jornada_semana_hhmm,
        'total_horas_bocadillo_semana': total_horas_bocadillo_semana_hhmm,
        'total_horas_salida_extra_semana': total_horas_salida_extra_semana_hhmm,
        'total_horas_trabajadas_semana': total_horas_trabajadas_semana_hhmm,
        'datos_diarios': datos_diarios_json,
    }

    return context, entorno


@login_required
def horas_informe_mensual(request, context):
    # Informe MENSUAL
    mensaje = ''
    fecha_str = request.POST.get('fecha_picker')
    fecha_seleccionada = datetime.strptime(fecha_str, '%Y-%m-%d').date()

    # Calcula el primer día del mes y el último día del mes seleccionado
    primer_dia_mes = fecha_seleccionada.replace(day=1)
    ultimo_dia_mes = fecha_seleccionada.replace(day=calendar.monthrange(fecha_seleccionada.year, fecha_seleccionada.month)[1])

    horas_informe_list = []
    total_dias_trabajados = 0  # Contador de días trabajados
    horas_diarias = 8  # Número de horas laborales diarias

    total_horas_jornada_mes = 0
    total_horas_bocadillo_mes = 0
    total_horas_salida_extra_mes = 0
    total_horas_trabajadas_mes = 0

    # Crear un único registro por fecha con valores acumulativos
    for dia in range((ultimo_dia_mes - primer_dia_mes).days + 1):
        fecha_actual = primer_dia_mes + timedelta(days=dia)
        registros_dia = Horas.objects.filter(fecha=fecha_actual)

        if registros_dia.exists():
            j0 = registros_dia.filter(tipo='J0').first()
            j1 = registros_dia.filter(tipo='J1').first()
            b0 = registros_dia.filter(tipo='B0').first()
            b1 = registros_dia.filter(tipo='B1').first()
            s0 = registros_dia.filter(tipo='S0').first()
            s1 = registros_dia.filter(tipo='S1').first()

            if j0 and j1:
                j_hora_inicio = datetime.combine(datetime.now().date(), j0.hora)
                j_hora_fin = datetime.combine(datetime.now().date(), j1.hora)
                total_jornada = (j_hora_fin - j_hora_inicio).total_seconds() / 3600
            else:
                total_jornada = 0

            if b0 and b1:
                b_hora_inicio = datetime.combine(datetime.now().date(), b0.hora)
                b_hora_fin = datetime.combine(datetime.now().date(), b1.hora)
                total_bocadillo = (b_hora_fin - b_hora_inicio).total_seconds() / 3600
            else:
                total_bocadillo = 0

            if s0 and s1:
                s_hora_inicio = datetime.combine(datetime.now().date(), s0.hora)
                s_hora_fin = datetime.combine(datetime.now().date(), s1.hora)
                total_salida_extra = (s_hora_fin - s_hora_inicio).total_seconds() / 3600
            else:
                total_salida_extra = 0

            horas_trabajadas = total_jornada - total_salida_extra

            # Calcular bocadillo según reglas
            if total_bocadillo > 0.5:
                horas_trabajadas -= (total_bocadillo - 0.5) 
            elif total_bocadillo < 0.5:
                horas_trabajadas += (0.5 - total_bocadillo) 

            total_jornada_hhmmss = "{:02d}:{:02d}:{:02d}".format(
                int(total_jornada),
                int((total_jornada % 1) * 60),
                int((total_jornada * 3600) % 60)
            )

            total_bocadillo_hhmmss = "{:02d}:{:02d}:{:02d}".format(
                int(total_bocadillo),
                int((total_bocadillo % 1) * 60),
                int((total_bocadillo * 3600) % 60)
            )

            total_salida_extra_hhmmss = "{:02d}:{:02d}:{:02d}".format(
                int(total_salida_extra),
                int((total_salida_extra % 1) * 60),
                int((total_salida_extra * 3600) % 60)
            )

            if horas_trabajadas >= horas_diarias:
                eficiencia_laboral_hhmmss = "{:02d}:{:02d}:{:02d}".format(
                    int((horas_trabajadas - horas_diarias) // 1),
                    int(((horas_trabajadas - horas_diarias) % 1) * 60),
                    int(((horas_trabajadas - horas_diarias) * 3600) % 60))
            else:
                eficiencia_laboral_hhmmss = "-{:02d}:{:02d}:{:02d}".format(
                    int((horas_diarias - horas_trabajadas) // 1),
                    int(((horas_diarias - horas_trabajadas) % 1) * 60),
                    int(((horas_diarias - horas_trabajadas) * 3600) % 60))

            horas_informe_list.append({
                'fecha': fecha_actual.strftime('%d/%m/%Y'),
                'total_jornada': total_jornada_hhmmss,
                'total_bocadillo': total_bocadillo_hhmmss,
                'total_salida_extra': total_salida_extra_hhmmss,
                'horas_trabajadas': "{:02d}:{:02d}:{:02d}".format(
                    int(horas_trabajadas),
                    int((horas_trabajadas % 1) * 60),
                    int((horas_trabajadas * 3600) % 60)
                ),
                'eficiencia_laboral_hhmmss': eficiencia_laboral_hhmmss
            })

            total_horas_jornada_mes += total_jornada
            total_horas_bocadillo_mes += total_bocadillo
            total_horas_salida_extra_mes += total_salida_extra
            total_horas_trabajadas_mes += horas_trabajadas

            if total_jornada > 0:
                total_dias_trabajados += 1

    # Calcular horas útiles y diferencia
    horas_utiles_mes = total_dias_trabajados * horas_diarias
    if horas_utiles_mes > total_horas_trabajadas_mes:
        diferencia_mes_class = "text_danger"
    else:
        diferencia_mes_class = "text_green"

    diferencia_mes = (horas_utiles_mes * 3600) - total_horas_trabajadas_mes * 3600

    # Formatear los totales mensuales
    total_horas_jornada_mes_hhmm = "{:02d}:{:02d}".format(
        int(total_horas_jornada_mes),
        int((total_horas_jornada_mes % 1) * 60)
    )
    total_horas_bocadillo_mes_hhmm = "{:02d}:{:02d}".format(
        int(total_horas_bocadillo_mes),
        int((total_horas_bocadillo_mes % 1) * 60)
    )
    total_horas_salida_extra_mes_hhmm = "{:02d}:{:02d}".format(
        int(total_horas_salida_extra_mes),
        int((total_horas_salida_extra_mes % 1) * 60)
    )
    total_horas_trabajadas_mes_hhmm = "{:02d}:{:02d}".format(
        int(total_horas_trabajadas_mes),
        int((total_horas_trabajadas_mes % 1) * 60)
    )
    diferencia_mes_hhmm = "{:02d}:{:02d}:{:02d}".format(
            int(diferencia_mes // 3600),
            int((diferencia_mes % 3600) // 60),
            int(diferencia_mes % 60)
    )
    horas_utiles_mes_hhmm = "{:02d}:{:02d}".format(
        int(horas_utiles_mes),
        int((horas_utiles_mes % 1) * 60)
    )
    
    # Crear una lista de meses para mostrar en ultimo_dia_mesla vista
    meses = [
        'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
        'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
    ]

    mes_actual = meses[fecha_seleccionada.month - 1]
    anio_actual = fecha_seleccionada.year

    # Agregar datos para la gráfica mensual
    # (Agrega esta sección al contexto con tus datos mensuales para la gráfica)

    # Inicializar una lista vacía para los datos mensuales
    datos_mensuales = []

    for dia in range(1, (ultimo_dia_mes.day) + 1):
        fecha_actual = fecha_seleccionada.replace(day=dia)

        # Buscar la entrada correspondiente en 'horas_informe_list' según la fecha
        entrada_dia = next((dia_info for dia_info in horas_informe_list if dia_info['fecha'] == fecha_actual.strftime('%d/%m/%Y')), None)

        if entrada_dia:
            # Si se encuentra una entrada correspondiente en 'horas_informe_list', usa esos datos
            datos_dia = {
                'nombre_dia': fecha_actual.strftime('%d/%m'),
                'datos': [
                    {'tipo': 'horas_trabajadas', 'valor': entrada_dia['total_jornada']},
                    {'tipo': 'bocadillos', 'valor': entrada_dia['total_bocadillo']},
                    {'tipo': 'salidas_extras', 'valor': entrada_dia['total_salida_extra']},
                    {'tipo': 'rendimiento', 'valor': entrada_dia['horas_trabajadas']},
                ]
            }
        else:
            # Si no se encuentra una entrada, usa valores predeterminados o en blanco
            datos_dia = {
                'nombre_dia': fecha_actual.strftime('%d/%m'),
                'datos': [
                    {'tipo': 'horas_trabajadas', 'valor': '00:00:00'},
                    {'tipo': 'bocadillos', 'valor': '00:00:00'},
                    {'tipo': 'salidas_extras', 'valor': '00:00:00'},
                    {'tipo': 'rendimiento', 'valor': '00:00:00'},
                ]
            }

        datos_mensuales.append(datos_dia)

    entorno = {
        'mensaje': mensaje,
        'fecha_inicio': primer_dia_mes.strftime('%d/%m/%Y'),
        'fecha_fin': ultimo_dia_mes.strftime('%d/%m/%Y'),
        'mes_actual': mes_actual,
        'anio_actual': anio_actual,
    }

    datos_mensuales_json = json.dumps(datos_mensuales)

    context = {
        'horas_informe_list': horas_informe_list,
        'total_dias_trabajados': total_dias_trabajados,
        'total_horas_jornada_mes': total_horas_jornada_mes_hhmm,
        'total_horas_bocadillo_mes': total_horas_bocadillo_mes_hhmm,
        'total_horas_salida_extra_mes': total_horas_salida_extra_mes_hhmm,
        'total_horas_trabajadas_mes': total_horas_trabajadas_mes_hhmm,
        'horas_utiles_mes':horas_utiles_mes_hhmm,
        'datos_diarios': datos_mensuales_json,
        'diferencia_mes': diferencia_mes_hhmm,
        'diferencia_mes_class': diferencia_mes_class,

    }

    return context, entorno


def horas_informe_rango(request, context):
    # Informe DE RANGO DE FECHAS
    mensaje = ''
    fecha_ini_str = request.POST.get('fecha_inicio')
    fecha_fin_str = request.POST.get('fecha_fin')

    fecha_inicio = datetime.strptime(fecha_ini_str, '%Y-%m-%d').date()
    fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()

    horas_informe_list = []
    total_dias_trabajados = 0  # Contador de días trabajados
    horas_diarias = 8  # Número de horas laborales diarias

    total_horas_jornada_mes = 0
    total_horas_bocadillo_mes = 0
    total_horas_salida_extra_mes = 0
    total_horas_trabajadas_mes = 0

    for dia in range((fecha_fin - fecha_inicio).days + 1):
        fecha_actual = fecha_inicio + timedelta(days=dia)
        registros_dia = Horas.objects.filter(fecha=fecha_actual)

        if registros_dia.exists():
            j0 = registros_dia.filter(tipo='J0').first()
            j1 = registros_dia.filter(tipo='J1').first()
            b0 = registros_dia.filter(tipo='B0').first()
            b1 = registros_dia.filter(tipo='B1').first()
            s0 = registros_dia.filter(tipo='S0').first()
            s1 = registros_dia.filter(tipo='S1').first()

            if j0 and j1:
                j_hora_inicio = datetime.combine(datetime.now().date(), j0.hora)
                j_hora_fin = datetime.combine(datetime.now().date(), j1.hora)
                total_jornada = (j_hora_fin - j_hora_inicio).total_seconds() / 3600
            else:
                total_jornada = 0

            if b0 and b1:
                b_hora_inicio = datetime.combine(datetime.now().date(), b0.hora)
                b_hora_fin = datetime.combine(datetime.now().date(), b1.hora)
                total_bocadillo = (b_hora_fin - b_hora_inicio).total_seconds() / 3600
            else:
                total_bocadillo = 0

            if s0 and s1:
                s_hora_inicio = datetime.combine(datetime.now().date(), s0.hora)
                s_hora_fin = datetime.combine(datetime.now().date(), s1.hora)
                total_salida_extra = (s_hora_fin - s_hora_inicio).total_seconds() / 3600
            else:
                total_salida_extra = 0

            horas_trabajadas = total_jornada - total_salida_extra

            # Calcular bocadillo según reglas
            if total_bocadillo > 0.5:
                horas_trabajadas -= (total_bocadillo - 0.5)
            elif total_bocadillo < 0.5:
                horas_trabajadas += (0.5 - total_bocadillo)

            total_jornada_hhmmss = "{:02d}:{:02d}:{:02d}".format(
                int(total_jornada),
                int((total_jornada % 1) * 60),
                int((total_jornada * 3600) % 60)
            )

            total_bocadillo_hhmmss = "{:02d}:{:02d}:{:02d}".format(
                int(total_bocadillo),
                int((total_bocadillo % 1) * 60),
                int((total_bocadillo * 3600) % 60)
            )

            total_salida_extra_hhmmss = "{:02d}:{:02d}:{:02d}".format(
                int(total_salida_extra),
                int((total_salida_extra % 1) * 60),
                int((total_salida_extra * 3600) % 60)
            )

            if horas_trabajadas >= horas_diarias:
                eficiencia_laboral_hhmmss = "{:02d}:{:02d}:{:02d}".format(
                    int((horas_trabajadas - horas_diarias) // 1),
                    int(((horas_trabajadas - horas_diarias) % 1) * 60),
                    int(((horas_trabajadas - horas_diarias) * 3600) % 60))
            else:
                eficiencia_laboral_hhmmss = "-{:02d}:{:02d}:{:02d}".format(
                    int((horas_diarias - horas_trabajadas) // 1),
                    int(((horas_diarias - horas_trabajadas) % 1) * 60),
                    int(((horas_diarias - horas_trabajadas) * 3600) % 60))

            horas_informe_list.append({
                'fecha': fecha_actual.strftime('%d/%m/%Y'),
                'total_jornada': total_jornada_hhmmss,
                'total_bocadillo': total_bocadillo_hhmmss,
                'total_salida_extra': total_salida_extra_hhmmss,
                'horas_trabajadas': "{:02d}:{:02d}:{:02d}".format(
                    int(horas_trabajadas),
                    int((horas_trabajadas % 1) * 60),
                    int((horas_trabajadas * 3600) % 60)
                ),
                'eficiencia_laboral_hhmmss': eficiencia_laboral_hhmmss
            })

            total_horas_jornada_mes += total_jornada
            total_horas_bocadillo_mes += total_bocadillo
            total_horas_salida_extra_mes += total_salida_extra
            total_horas_trabajadas_mes += horas_trabajadas

            if total_jornada > 0:
                total_dias_trabajados += 1

    # Calcular horas útiles y diferencia
    horas_utiles_mes = total_dias_trabajados * horas_diarias
    if horas_utiles_mes > total_horas_trabajadas_mes:
        diferencia_mes_class = "text_danger"
    else:
        diferencia_mes_class = "text_green"

    diferencia_mes = (horas_utiles_mes * 3600) - total_horas_trabajadas_mes * 3600

    # Formatear los totales mensuales
    total_horas_jornada_mes_hhmm = "{:02d}:{:02d}".format(
        int(total_horas_jornada_mes),
        int((total_horas_jornada_mes % 1) * 60)
    )
    total_horas_bocadillo_mes_hhmm = "{:02d}:{:02d}".format(
        int(total_horas_bocadillo_mes),
        int((total_horas_bocadillo_mes % 1) * 60)
    )
    total_horas_salida_extra_mes_hhmm = "{:02d}:{:02d}".format(
        int(total_horas_salida_extra_mes),
        int((total_horas_salida_extra_mes % 1) * 60)
    )
    total_horas_trabajadas_mes_hhmm = "{:02d}:{:02d}".format(
        int(total_horas_trabajadas_mes),
        int((total_horas_trabajadas_mes % 1) * 60)
    )
    diferencia_mes_hhmm = "{:02d}:{:02d}:{:02d}".format(
        int(diferencia_mes // 3600),
        int((diferencia_mes % 3600) // 60),
        int(diferencia_mes % 60)
    )
    horas_utiles_mes_hhmm = "{:02d}:{:02d}".format(
        int(horas_utiles_mes),
        int((horas_utiles_mes % 1) * 60)
    )

    # Crear una lista de meses para mostrar en la vista
    meses = [
        'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
        'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
    ]

    # Crear una lista de días para mostrar en la vista
    dias = [fecha_inicio + timedelta(days=i) for i in range((fecha_fin - fecha_inicio).days + 1)]

    # Agregar datos para la gráfica mensual
    datos_diarios = []
    for dia in dias:
        # Buscar la entrada correspondiente en 'horas_informe_list' según la fecha
        entrada_dia = next((dia_info for dia_info in horas_informe_list if dia_info['fecha'] == dia.strftime('%d/%m/%Y')), None)

        if entrada_dia:
            # Si se encuentra una entrada correspondiente en 'horas_informe_list', usa esos datos
            datos_dia = {
                'nombre_dia': fecha_actual.strftime('%d/%m'),
                'datos': [
                    {'tipo': 'horas_trabajadas', 'valor': entrada_dia['total_jornada']},
                    {'tipo': 'bocadillos', 'valor': entrada_dia['total_bocadillo']},
                    {'tipo': 'salidas_extras', 'valor': entrada_dia['total_salida_extra']},
                    {'tipo': 'rendimiento', 'valor': entrada_dia['horas_trabajadas']},
                ]
            }
        else:
            # Si no se encuentra una entrada, usa valores predeterminados o en blanco
            datos_dia = {
                'nombre_dia': fecha_actual.strftime('%d/%m'),
                'datos': [
                    {'tipo': 'horas_trabajadas', 'valor': '00:00:00'},
                    {'tipo': 'bocadillos', 'valor': '00:00:00'},
                    {'tipo': 'salidas_extras', 'valor': '00:00:00'},
                    {'tipo': 'rendimiento', 'valor': '00:00:00'},
                ]
            }

        datos_diarios.append(datos_dia)

    entorno = {
        'mensaje': mensaje,
        'fecha_inicio': fecha_inicio.strftime('%d/%m/%Y'),
        'fecha_fin': fecha_fin.strftime('%d/%m/%Y'),
    }

    datos_diarios_json = json.dumps(datos_diarios)

    context = {
        'horas_informe_list': horas_informe_list,
        'datos_diarios': datos_diarios_json,
        'total_dias_trabajados': total_dias_trabajados,
        'total_horas_jornada_mes': total_horas_jornada_mes_hhmm,
        'total_horas_bocadillo_mes': total_horas_bocadillo_mes_hhmm,
        'total_horas_salida_extra_mes': total_horas_salida_extra_mes_hhmm,
        'total_horas_trabajadas_mes': total_horas_trabajadas_mes_hhmm,
        'horas_utiles_mes': horas_utiles_mes_hhmm,
        'diferencia_mes': diferencia_mes_hhmm,
        'diferencia_mes_class': diferencia_mes_class,
    }

    #print("DATOS = " + str(datos_diarios))

    #print("JSON = " + str(datos_diarios_json))
          
    return context, entorno


def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            # registrar usuario
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save
                login(request, user)
                return redirect('home2')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": 'El nombre de usuario ya existe'
                })

        return render(request, 'signup.html', {
            'form': UserCreationForm,
            "error": 'La contraseña no coincide'
        })


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'El usuario o la contraseña no son correctos'
            })
        else:
            if user.is_staff == 1:
                login(request, user)
                return redirect('home')
            else:
                login(request, user)
                return redirect('home2')


@login_required
def signout(request):  # no uso logout de nombre porque crearía conflicto
    logout(request)
    return redirect('home')


@login_required
@user_passes_test(is_superuser, login_url='home2')
def clientes(request):
    filtro_form = FiltroForm(request.GET or None)

    if filtro_form.is_valid():
        filtro = filtro_form.cleaned_data['filtro']
        if filtro == 'todos':
            clientes = Clientes.objects.all()
        elif filtro == 'activos':
            clientes = Clientes.objects.filter(activo=True)
        elif filtro == 'no_activos':
            clientes = Clientes.objects.filter(activo=False)
        else:
            clientes = Clientes.objects.all()  # Cambio realizado aquí
    else:
        clientes = Clientes.objects.all()

    page = request.GET.get('page', 1)
    try:
        paginator = Paginator(clientes, 10)
        clientes = paginator.page(page)
    except ValueError:
        raise Http404

    data = {
        'entity': clientes,
        'paginator': paginator,
        'filtro_form': filtro_form,
    }

    return render(request, 'clientes.html', data)


@login_required
@user_passes_test(is_superuser, login_url='home2')
def cliente_detalle(request, cliente_id):
    if request.method == 'GET':
        cliente = get_object_or_404(Clientes, pk=cliente_id)
        form = ClienteForm(instance=cliente)
        return render(request, 'cliente_detalle.html', {'cliente': cliente, 'form': form})
    else:
        try:
            cliente = get_object_or_404(Clientes, pk=cliente_id)
            form = ClienteForm(request.POST, instance=cliente)
            form.save()
            return redirect('clientes')
        except ValueError:
            return render(request, 'cliente_detalle.html', {'cliente': cliente, 'form': form, 'error': "Ocurrió un error en la actualización"})


@login_required
@user_passes_test(is_superuser, login_url='home2')
def crear_cliente(request):

    if request.method == 'GET':
        return render(request, 'crear_cliente.html', {
            'form': ClienteForm
        })
    else:
        try:
            form = ClienteForm(request.POST)  # Me traigo el form de form.py
            form.save()
            return redirect('clientes')
        except ValueError:
            return render(request, 'crear_cliente.html', {
                'form': ClienteForm,
                'error': 'Los datos no son validos'
            })


@login_required
@user_passes_test(is_superuser, login_url='home2')
def cliente_eliminar(request, cliente_id):
    cliente = get_object_or_404(Clientes, pk=cliente_id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('clientes')


@login_required
@user_passes_test(is_superuser, login_url='home2')
def obras(request):
    filtro_form = FiltroForm(request.GET or None)

    if filtro_form.is_valid():
        filtro = filtro_form.cleaned_data['filtro']
        if filtro == 'todos':
            obras = Obras.objects.all()
        elif filtro == 'activos':
            obras = Obras.objects.filter(activo=True)
        elif filtro == 'no_activos':
            obras = Obras.objects.filter(activo=False)
        else:
            obras = Obras.objects.all()
    else:
        obras = Obras.objects.all()

    page = request.GET.get('page', 1)
    try:
        paginator = Paginator(obras, 10)
        obras = paginator.page(page)
    except ValueError:
        raise Http404

    data = {
        'entity': obras,
        'paginator': paginator,
        'filtro_form': FiltroForm(),  # Cambio realizado aquí
    }

    return render(request, 'obras.html', data)


@login_required
@user_passes_test(is_superuser, login_url='home2')
def obra_crear(request):

    if request.method == 'GET':
        return render(request, 'obra_crear.html', {
            'form': ObrasForm
        })
    else:
        try:
            form = ObrasForm(request.POST)
            form.save()
            return redirect('obras')
        except ValueError:
            return render(request, 'obra_crear.html', {
                'form': ObrasForm,
                'error': 'Los datos no son validos'
            })


@login_required
@user_passes_test(is_superuser, login_url='home2')
def obra_detalle(request, obra_id):
    if request.method == 'GET':
        obra = get_object_or_404(Obras, pk=obra_id)
        form = ObrasForm(instance=obra)
        return render(request, 'obra_detalle.html', {'obra': obra, 'form': form})
    else:
        try:
            obra = get_object_or_404(Obras, pk=obra_id)
            form = ObrasForm(request.POST, instance=obra)
            form.save()
            return redirect('obras')
        except ValueError:
            return render(request, 'obra_detalle.html', {'obra': obra, 'form': form, 'error': "Ocurrió un error en la actualización"})


@login_required
@user_passes_test(is_superuser, login_url='home2')
def obra_eliminar(request, obra_id):
    obra = get_object_or_404(Obras, pk=obra_id)
    if request.method == 'POST':
        obra.delete()
        return redirect('obras')


@login_required
@user_passes_test(is_superuser, login_url='home2')
def materialesf(request):
    filtro_form = FiltroForm(request.GET or None)

    if filtro_form.is_valid():
        filtro = filtro_form.cleaned_data['filtro']
        if filtro == 'todos':
            materialesf = MaterialesF.objects.all()
        elif filtro == 'activos':
            materialesf = MaterialesF.objects.filter(activo=True)
        elif filtro == 'no_activos':
            materialesf = MaterialesF.objects.filter(activo=False)
        else:
            materialesf = MaterialesF.objects.all()
    else:
        materialesf = MaterialesF.objects.all()

    page = request.GET.get('page', 1)
    try:
        paginator = Paginator(materialesf, 10)
        materialesf = paginator.page(page)
    except ValueError:
        raise Http404

    data = {
        'entity': materialesf,
        'paginator': paginator,
        'filtro_form': filtro_form,
    }

    return render(request, 'materialesf.html', data)


@login_required
@user_passes_test(is_superuser, login_url='home2')
def materialf_crear(request):

    if request.method == 'GET':
        return render(request, 'materialf_crear.html', {
            'form': MaterialesfForm
        })
    else:
        try:
            form = MaterialesfForm(request.POST)
            form.save()
            return redirect('materialesf')
        except ValueError:
            return render(request, 'materialf_crear.html', {
                'form': MaterialesfForm,
                'error': 'Los datos no son validos'
            })


@login_required
@user_passes_test(is_superuser, login_url='home2')
def materialf_detalle(request, materialf_id):
    if request.method == 'GET':
        materialf = get_object_or_404(MaterialesF, pk=materialf_id)
        form = MaterialesfForm(instance=materialf)
        return render(request, 'materialf_detalle.html', {'materialf': materialf, 'form': form})
    else:
        try:
            materialf = get_object_or_404(MaterialesF, pk=materialf_id)
            #print(materialf_id)
            form = MaterialesfForm(request.POST, instance=materialf)
            #print(form)
            form.save()
            return redirect('materialesf')
        except ValueError:
            return render(request, 'materialf_detalle.html', {'materialf': materialf, 'form': form, 'error': "Ocurrió un error en la actualización"})


@login_required
@user_passes_test(is_superuser, login_url='home2')
def materialf_eliminar(request, materialf_id):
    materialf = get_object_or_404(MaterialesF, pk=materialf_id)
    if request.method == 'POST':
        materialf.delete()
        return redirect('materialesf')


@login_required
@user_passes_test(is_superuser, login_url='home2')
def materiales(request):
    filtro_form = FiltroForm(request.GET or None)

    if filtro_form.is_valid():
        filtro = filtro_form.cleaned_data['filtro']
        if filtro == 'todos':
            materiales = Materiales.objects.all()
        elif filtro == 'activos':
            materiales = Materiales.objects.filter(activo=True)
        elif filtro == 'no_activos':
            materiales = Materiales.objects.filter(activo=False)
        else:
            materiales = Materiales.objects.all()
    else:
        materiales = Materiales.objects.all()

    page = request.GET.get('page', 1)
    try:
        paginator = Paginator(materiales, 10)
        materiales = paginator.page(page)
    except ValueError:
        raise Http404

    data = {
        'entity': materiales,
        'paginator': paginator,
        'filtro_form': filtro_form,
    }

    return render(request, 'materiales.html', data)


@login_required
@user_passes_test(is_superuser, login_url='home2')
def material_crear(request):

    if request.method == 'GET':
        return render(request, 'material_crear.html', {
            'form': MaterialesForm
        })
    else:
        try:
            form = MaterialesForm(request.POST)
            form.save()
            return redirect('materialesf')
        except ValueError:
            return render(request, 'material_crear.html', {
                'form': MaterialesForm,
                'error': 'Los datos no son validos'
            })


@login_required
@user_passes_test(is_superuser, login_url='home2')
def material_detalle(request, material_id):
    if request.method == 'GET':
        material = get_object_or_404(Materiales, pk=material_id)
        #print(material)
        form = MaterialesForm(instance=material)
        return render(request, 'material_detalle.html', {'material': material, 'form': form})
    else:
        try:
            material = get_object_or_404(Materiales, pk=material_id)
            form = MaterialesForm(request.POST, instance=material)
            form.save()
            return redirect('materiales')
        except ValueError:
            return render(request, 'material_detalle.html', {'material': material, 'form': form, 'error': "Ocurrió un error en la actualización"})


@login_required
@user_passes_test(is_superuser, login_url='home2')
def material_eliminar(request, material_id):
    material = get_object_or_404(Materiales, pk=material_id)
    if request.method == 'POST':
        material.delete()
        return redirect('materiales')


@login_required
@user_passes_test(is_superuser, login_url='home2')
def usuarios(request):
    filtro_form = FiltroForm(request.GET or None)

    if filtro_form.is_valid():
        filtro = filtro_form.cleaned_data['filtro']
        if filtro == 'todos':
            usuarios = User.objects.all()
        elif filtro == 'activos':
            usuarios = User.objects.filter(is_active=1)
        elif filtro == 'no_activos':
            usuarios = User.objects.filter(is_active=0)
        else:
            usuarios = User.objects.all()
    else:
        usuarios = User.objects.all()

    page = request.GET.get('page', 1)
    try:
        paginator = Paginator(usuarios, 10)
        usuarios = paginator.page(page)
    except ValueError:
        raise Http404

    data = {
        'entity': usuarios,
        'paginator': paginator,
        'filtro_form': filtro_form,
    }

    return render(request, 'usuarios.html', data)


@login_required
@user_passes_test(is_superuser, login_url='home2')
def usuario_crear(request):
    form = UsuarioNuevoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('usuarios')
    return render(request, 'usuario_crear.html', {'form': form,
                                                  'error': 'Los datos no son validos'})


@login_required
@user_passes_test(is_superuser, login_url='home2')
def usuario_editar(request, usuario_id):
    user = User.objects.get(pk=usuario_id)
    form = UsuarioEditarForm(request.POST or None, instance=user)

    if form.is_valid():
        # Guardar los campos comunes del usuario
        user.username = form.cleaned_data['username']
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.email = form.cleaned_data['email']
        user.is_superuser = form.cleaned_data['is_superuser']
        user.is_active = form.cleaned_data['is_active']

        # Verificar si se proporcionó una nueva contraseña
        password1 = form.cleaned_data['password1']
        password2 = form.cleaned_data['password2']
        if password1 and password2 and password1 == password2:
            # Cambiar la contraseña solo si se proporcionó y coincide la confirmación
            user.set_password(password1)

        # Guardar el usuario
        user.save()

        return redirect('usuarios')

    return render(request, 'usuario_detalle.html', {'form': form, 'user': user})


@login_required
@user_passes_test(is_superuser, login_url='home2')
def usuario_eliminar(request, usuario_id):
    user = User.objects.get(pk=usuario_id)
    user.delete()
    return redirect('usuarios')
