import pygame as pg

def inicializar_wish_icons(form):
    """Inicializa los iconos de wishes en el formulario"""
    form['wish_icons'] = {
        'heal': {
            'imagen': None,
            'disponible': True,
            'activo': False,
            'pos_disponible': (1140, 558),
            'pos_activo': (1140, 176),
            'pos_actual': (1140, 558),
            'animando_movimiento': False,
            'tiempo_animacion': 0,
            'duracion_animacion': 500,
            'pos_inicial': (1140, 558),
            'pos_destino': (1140, 176)
        },
        'shield': {
            'imagen': None,
            'disponible': True,
            'activo': False,
            'pos_disponible': (1200, 558),
            'pos_activo': (1200, 176),
            'pos_actual': (1200, 558),
            'animando_movimiento': False,
            'tiempo_animacion': 0,
            'duracion_animacion': 500,
            'pos_inicial': (1200, 558),
            'pos_destino': (1200, 176)
        }
    }

    try:
        heal_img = pg.image.load('./assets_Dragon_Ball_Trading_Card_Game/img/icons/icon_heal.png')
        shield_img = pg.image.load('./assets_Dragon_Ball_Trading_Card_Game/img/icons/icon_shield.png')

        form['wish_icons']['heal']['imagen'] = pg.transform.scale(heal_img, (50, 50))
        form['wish_icons']['shield']['imagen'] = pg.transform.scale(shield_img, (50, 50))
    except Exception as e:
        print(f"Error cargando iconos de wishes: {e}")

def select_wish(form_y_bonus_name):
    """Maneja la selección de un wish"""
    form = form_y_bonus_name.get('form')
    wish_type = form_y_bonus_name.get('wish')
    jugador = form['level']['jugador']

    if wish_type == 'HEAL' and jugador.get('heal_usado', False):
        return

    if wish_type == 'SHIELD' and jugador.get('shield_usado', False):
        return

    activar_wish_icon(form, wish_type)

    if wish_type == 'HEAL':
        jugador['hp'] = jugador.get('hp_inicial', jugador['hp'])
        jugador['heal_usado'] = True

        try:
            sonido_heal = pg.mixer.Sound('./assets_Dragon_Ball_Trading_Card_Game/audio/sounds/heal_activated.ogg')
            sonido_heal.play()
        except Exception as e:
            pass

    elif wish_type == 'SHIELD':
        jugador['shield_activo'] = True
        jugador['shield_usado'] = True

        try:
            sonido_shield = pg.mixer.Sound('./assets_Dragon_Ball_Trading_Card_Game/audio/sounds/shield_activated.ogg')
            sonido_shield.play()
        except Exception as e:
            pass

def dibujar_wish_icons(form_data):
    """Dibuja los iconos de wishes en sus posiciones actuales"""
    jugador = form_data.get('jugador', {})

    for wish_type, wish_info in form_data['wish_icons'].items():
        if wish_info['imagen'] and wish_info['disponible']:
            pos = wish_info['pos_actual']

            form_data['screen'].blit(wish_info['imagen'], pos)

            if wish_type == 'shield' and wish_info['activo'] and jugador.get('shield_activo', False):
                rect = pg.Rect(pos[0]-3, pos[1]-3, 56, 56)
                pg.draw.rect(form_data['screen'], (255, 215, 0), rect, 4)
            else:
                rect = pg.Rect(pos[0]-2, pos[1]-2, 54, 54)
                pg.draw.rect(form_data['screen'], (100, 100, 100), rect, 2)

def activar_wish_icon(form_data, wish_type):
    """Mueve el icono de wish del área 'available' al área 'active' con animación"""
    if wish_type.lower() in form_data['wish_icons']:
        wish_info = form_data['wish_icons'][wish_type.lower()]

        wish_info['activo'] = True

        wish_info['animando_movimiento'] = True
        wish_info['tiempo_animacion'] = 0
        wish_info['duracion_animacion'] = 500
        wish_info['pos_inicial'] = wish_info['pos_actual']
        wish_info['pos_destino'] = wish_info['pos_activo']

        jugador = form_data.get('jugador')
        if jugador:
            if wish_type.lower() == 'heal':
                jugador['heal_usado'] = True
            elif wish_type.lower() == 'shield':
                jugador['shield_usado'] = True

def actualizar_wish_icons(form_data):
    """Actualiza el estado de los iconos de wishes según el estado del jugador"""
    jugador = form_data.get('jugador')
    if not jugador:
        return

    if jugador.get('heal_usado', False):
        form_data['wish_icons']['heal']['disponible'] = False

    if jugador.get('shield_usado', False):
        form_data['wish_icons']['shield']['disponible'] = False

    if jugador.get('shield_activo', False):
        form_data['wish_icons']['shield']['activo'] = True
        form_data['wish_icons']['shield']['pos_actual'] = form_data['wish_icons']['shield']['pos_activo']
    else:
        if form_data['wish_icons']['shield']['activo']:
            form_data['wish_icons']['shield']['activo'] = False

def update_wish_icons(form_data, delta_time):
    """Actualiza las animaciones de los iconos de wish"""
    for wish_type, wish_info in form_data['wish_icons'].items():
        if wish_info['animando_movimiento']:
            wish_info['tiempo_animacion'] += delta_time

            progreso = min(wish_info['tiempo_animacion'] / wish_info['duracion_animacion'], 1.0)

            progreso_suave = 1 - pow(1 - progreso, 3)

            pos_inicial = wish_info['pos_inicial']
            pos_destino = wish_info['pos_destino']

            wish_info['pos_actual'] = (
                pos_inicial[0] + (pos_destino[0] - pos_inicial[0]) * progreso_suave,
                pos_inicial[1] + (pos_destino[1] - pos_inicial[1]) * progreso_suave
            )

            if progreso >= 1.0:
                wish_info['animando_movimiento'] = False
                wish_info['pos_actual'] = pos_destino

def resetear_wishes(form):
    """Resetea los wishes al estado inicial para la próxima partida"""
    jugador = form.get('jugador')
    if jugador:
        jugador['heal_usado'] = False
        jugador['shield_usado'] = False
        jugador['shield_activo'] = False

    form['wish_icons']['heal']['disponible'] = True
    form['wish_icons']['heal']['activo'] = False
    form['wish_icons']['heal']['pos_actual'] = form['wish_icons']['heal']['pos_disponible']
    form['wish_icons']['heal']['animando_movimiento'] = False

    form['wish_icons']['shield']['disponible'] = True
    form['wish_icons']['shield']['activo'] = False
    form['wish_icons']['shield']['pos_actual'] = form['wish_icons']['shield']['pos_disponible']
    form['wish_icons']['shield']['animando_movimiento'] = False
