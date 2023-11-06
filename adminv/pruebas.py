@login_required
def marcar_tarjeta(request):
    usuario = request.user
    latitud = request.POST.get('latitud')
    longitud = request.POST.get('longitud')

    # Obtener el último registro de horario
    ultimo_horario = Horas.objects.filter(idUsuario=usuario).order_by('-fecha').first()

    if ultimo_horario is not None and ultimo_horario.tipo == 'entrada':
        tiempo_transcurrido = datetime.now() - datetime.combine(ultimo_horario.fecha, ultimo_horario.hora)
        if tiempo_transcurrido.total_seconds() >= 300:
            # Guardar las coordenadas en el campo 'coordenadas' del registro de horario
            ultimo_horario.coordenadas = f'{latitud},{longitud}'
            ultimo_horario.save()
            mensaje = 'Se ha registrado la salida correctamente.'
            boton_texto = 'Comenzar'
        else:
            tiempo_restante = timedelta(seconds=300) - tiempo_transcurrido
            mensaje = f'Aún no han pasado 5 minutos desde la entrada. Tiempo restante: {tiempo_restante}'
            boton_texto = 'Cerrar'
    else:
        # Crear un nuevo registro de horario y guardar las coordenadas
        nuevo_horario = Horas(fecha=datetime.now().date(), hora=datetime.now().time(), tipo='entrada', idUsuario=usuario, coordenadas=f'{latitud},{longitud}')
        nuevo_horario.save()
        mensaje = 'Se ha registrado la entrada correctamente.'
        boton_texto = 'Cerrar'

    contexto = {
        'mensaje': mensaje,
        'boton_texto': boton_texto
    }

    return render(request, 'home2.html', contexto)
