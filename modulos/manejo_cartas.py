import pygame as pg
import modulos.carta as carta_mod
import modulos.batalla as batalla

def calcular_stats_mazo(mazo):
    """Calcula las stats totales basadas en todas las cartas del mazo SIN bonus de estrellas"""
    if not mazo:
        return {'hp': 0, 'atk': 0, 'def': 0}

    total_hp = 0
    total_atk = 0
    total_def = 0

    for carta in mazo:
        total_hp += carta['hp']
        total_atk += carta['atk']
        total_def += carta['def']

    return {
        'hp': total_hp,
        'atk': total_atk,
        'def': total_def
    }

def inicializar_stats_jugadores(form):
    """Inicializa las stats de jugador y enemy basadas en la sumatoria de sus mazos"""
    level = form.get('level')
    jugador = form.get('jugador')
    enemy = form.get('enemy')

    if level and jugador and enemy:
        mazo_jugador = level.get('cartas_mazo_jugador', [])
        mazo_enemy = level.get('cartas_mazo_enemy', [])

        stats_iniciales_jugador = calcular_stats_mazo(mazo_jugador)
        stats_iniciales_enemy = calcular_stats_mazo(mazo_enemy)

        jugador['hp'] = stats_iniciales_jugador['hp']
        jugador['atk'] = stats_iniciales_jugador['atk']
        jugador['def'] = stats_iniciales_jugador['def']
        jugador['hp_inicial'] = stats_iniciales_jugador['hp']

        enemy['hp'] = stats_iniciales_enemy['hp']
        enemy['atk'] = stats_iniciales_enemy['atk']
        enemy['def'] = stats_iniciales_enemy['def']
        enemy['hp_inicial'] = stats_iniciales_enemy['hp']

        resetear_todas_animaciones(form)

def resetear_todas_animaciones(form_data):
    """Resetea todas las animaciones de cartas en el formulario"""
    cartas_jugador = form_data.get('level', {}).get('cartas_mazo_jugador_vistas', [])
    for carta in cartas_jugador:
        carta_mod.resetear_animacion_carta(carta)

    cartas_enemy = form_data.get('level', {}).get('cartas_mazo_enemy_vistas', [])
    for carta in cartas_enemy:
        carta_mod.resetear_animacion_carta(carta)

def actualizar_animaciones_cartas(form_data):
    """Actualiza las animaciones de choque de las cartas"""
    delta_time = form_data['clock'].get_time()

    cartas_jugador = form_data.get('level', {}).get('cartas_mazo_jugador_vistas', [])
    for carta in cartas_jugador:
        if carta.get('animando', False):
            carta_mod.actualizar_animacion_choque(carta, delta_time)
        if carta.get('animando_volando', False):
            carta_mod.actualizar_animacion_salir_volando(carta, delta_time)
        if carta.get('animando_entrada', False):
            carta_mod.actualizar_animacion_entrada(carta, delta_time)

    cartas_enemy = form_data.get('level', {}).get('cartas_mazo_enemy_vistas', [])
    for carta in cartas_enemy:
        if carta.get('animando', False):
            carta_mod.actualizar_animacion_choque(carta, delta_time)
        if carta.get('animando_volando', False):
            carta_mod.actualizar_animacion_salir_volando(carta, delta_time)
        if carta.get('animando_entrada', False):
            carta_mod.actualizar_animacion_entrada(carta, delta_time)

def hay_animaciones_en_curso(form):
    """Verifica si hay animaciones de choque en curso en cualquier carta"""
    cartas_jugador = form.get('level', {}).get('cartas_mazo_jugador_vistas', [])
    for carta in cartas_jugador:
        if (carta.get('animando', False) or
            carta.get('animando_volando', False) or
            carta.get('animando_entrada', False)):
            return True

    cartas_enemy = form.get('level', {}).get('cartas_mazo_enemy_vistas', [])
    for carta in cartas_enemy:
        if (carta.get('animando', False) or
            carta.get('animando_volando', False) or
            carta.get('animando_entrada', False)):
            return True

    return False

def mostrar_cartas_con_animacion(form):
    """Muestra las cartas del mazo con animación de entrada"""
    if form['level']['cartas_mazo_jugador']:
        carta_jugador = form['level']['cartas_mazo_jugador'][0]

        coords_mazo_jugador = form['level']['configs']['coordenadas']['mazo_jugador']
        pos_inicial_jugador = (coords_mazo_jugador['x'], coords_mazo_jugador['y'])

        carta_mod.asignar_coordenadas_carta(carta_jugador, pos_inicial_jugador)

        coords_jugada_jugador = form['level']['configs']['coordenadas']['jugada_jugador']
        pos_final_jugador = (coords_jugada_jugador['x'], coords_jugada_jugador['y'])

        carta_mod.iniciar_animacion_entrada(carta_jugador, pos_inicial_jugador, pos_final_jugador)
        carta_jugador['visible'] = True

        carta_vista_jugador = form['level']['cartas_mazo_jugador'].pop(0)
        form['level']['cartas_mazo_jugador_vistas'].append(carta_vista_jugador)

    if form['level']['cartas_mazo_enemy']:
        carta_enemy = form['level']['cartas_mazo_enemy'][0]

        coords_mazo_enemy = form['level']['configs']['coordenadas']['mazo_enemy']
        pos_inicial_enemy = (coords_mazo_enemy['x'], coords_mazo_enemy['y'])

        carta_mod.asignar_coordenadas_carta(carta_enemy, pos_inicial_enemy)

        coords_jugada_enemy = form['level']['configs']['coordenadas']['jugada_enemy']
        pos_final_enemy = (coords_jugada_enemy['x'], coords_jugada_enemy['y'])

        carta_mod.iniciar_animacion_entrada(carta_enemy, pos_inicial_enemy, pos_final_enemy)
        carta_enemy['visible'] = True

        carta_vista_enemy = form['level']['cartas_mazo_enemy'].pop(0)
        form['level']['cartas_mazo_enemy_vistas'].append(carta_vista_enemy)

def ejecutar_choque_batalla(form, actualizar_stats_callback=None):
    """Ejecuta la animación de choque basada en el resultado de la batalla y aplica los cambios"""
    resultado = form.get('resultado_batalla', {})

    if 'cambios' in resultado:
        batalla.aplicar_cambios_batalla(form['level'], resultado['cambios'])
        if actualizar_stats_callback:
            actualizar_stats_callback(form)

    if resultado.get('ganador') == 'empate':
        try:
            sonido_empate = pg.mixer.Sound('./assets_Dragon_Ball_Trading_Card_Game/audio/sounds/click.ogg')
            sonido_empate.play()
        except Exception as e:
            pass
    elif resultado.get('ganador') and resultado.get('ganador') != 'empate':
        carta_jugador_actual = form['level']['cartas_mazo_jugador_vistas'][-1]
        carta_enemy_actual = form['level']['cartas_mazo_enemy_vistas'][-1]

        if resultado.get('ganador') == 'jugador':
            carta_mod.iniciar_animacion_choque(carta_jugador_actual, carta_enemy_actual)
        elif resultado.get('ganador') == 'enemy':
            carta_mod.iniciar_animacion_choque(carta_enemy_actual, carta_jugador_actual)

    if resultado.get('batalla_terminada', {}).get('terminada', False):
        form['batalla_terminada'] = True

        import modulos.manejo_wishes as manejo_wishes
        manejo_wishes.resetear_wishes(form)

        ganador_batalla = resultado.get('batalla_terminada', {}).get('ganador')

        import modulos.forms.base_form as base_form
        base_form.stop_music()

        if ganador_batalla == "jugador":
            base_form.play_music(base_form.forms_dict['form_enter_name'])
            base_form.set_active('form_enter_name')
        elif ganador_batalla == "empate":
            base_form.play_music(base_form.forms_dict['form_defeat'])
            base_form.set_active('form_defeat')
        else:
            base_form.play_music(base_form.forms_dict['form_defeat'])
            base_form.set_active('form_defeat')

def remover_cartas_y_preparar_siguiente(form):
    """Remueve las cartas actuales y prepara para la siguiente ronda"""
    if form['level']['cartas_mazo_jugador_vistas']:
        carta_jugador = form['level']['cartas_mazo_jugador_vistas'][-1]
        carta_jugador['visible'] = False
        carta_mod.resetear_animacion_carta(carta_jugador)

    if form['level']['cartas_mazo_enemy_vistas']:
        carta_enemy = form['level']['cartas_mazo_enemy_vistas'][-1]
        carta_enemy['visible'] = False
        carta_mod.resetear_animacion_carta(carta_enemy)

    form['level']['cartas_mazo_jugador_vistas'] = [
        carta for carta in form['level']['cartas_mazo_jugador_vistas']
        if carta.get('visible', False) or carta.get('animando', False) or
           carta.get('animando_volando', False) or carta.get('animando_entrada', False)
    ]

    form['level']['cartas_mazo_enemy_vistas'] = [
        carta for carta in form['level']['cartas_mazo_enemy_vistas']
        if carta.get('visible', False) or carta.get('animando', False) or
           carta.get('animando_volando', False) or carta.get('animando_entrada', False)
    ]

    form['secuencia_batalla_activa'] = False
    form['choque_ejecutado'] = False
    form['tiempo_secuencia'] = 0

def iniciar_secuencia_batalla(form):
    """Inicia la secuencia completa de batalla con timing controlado"""
    form['secuencia_batalla_activa'] = True
    form['tiempo_secuencia'] = 0

    mostrar_cartas_con_animacion(form)

    form['resultado_batalla'] = batalla.calcular_resultado_batalla(form['level'])

def actualizar_secuencia_batalla(form, delta_time, actualizar_stats_callback=None):
    """Actualiza la secuencia de batalla: entrada 600ms → espera 500ms → choque 1000ms → remoción"""
    if not form.get('secuencia_batalla_activa', False):
        return

    form['tiempo_secuencia'] += delta_time

    if form['tiempo_secuencia'] >= 1100 and not form.get('choque_ejecutado', False):
        ejecutar_choque_batalla(form, actualizar_stats_callback)
        form['choque_ejecutado'] = True

    elif form['tiempo_secuencia'] >= 2600 and form.get('choque_ejecutado', False):
        remover_cartas_y_preparar_siguiente(form)
