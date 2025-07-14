import pygame as pg
import modulos.forms.base_form as base_form
import modulos.variables as var
import modulos.nivel_cartas as nivel_cartas
import modulos.forms.form_wish as form_wish
import modulos.batalla as batalla
import modulos.enemy as enemy
import modulos.jugador as jugador_mod
import modulos.manejo_cartas as manejo_cartas
import modulos.manejo_wishes as manejo_wishes
from utn_fra.pygame_widgets import (
    ButtonImage, Label, TextPoster, Button
)

def init_form_start_level(dict_form_data: dict, jugador: dict, enemy: dict):
    """
    Inicializa el formulario del nivel de juego
    
    Args:
        dict_form_data: Diccionario con los datos del formulario
        jugador: Diccionario con los datos del jugador
        enemy: Diccionario con los datos del enemigo
    
    Returns:
        dict: Formulario inicializado
    """
    form = base_form.create_base_form(dict_form_data)
    
    # Configurar jugador
    form['jugador'] = jugador
    
    # Configurar enemy
    if not form.get('enemy'):
        import modulos.enemy as enemy_mod
        form['enemy'] = enemy_mod.inicializar_enemy()
    
    # Inicializar nivel de cartas
    form['level'] = nivel_cartas.inicializar_nivel_cartas(
        form.get('jugador'),
        form.get('screen'),
        form.get('level_number'),
        form.get('enemy')
    )
    
    # Inicializar cartas actuales
    form['carta_jugador'] = None
    form['carta_enemy'] = None
    
    # Configurar reloj y timers
    form['clock'] = pg.time.Clock()
    form['first_last_timer'] = pg.time.get_ticks()
    form['bonus_1_used'] = False
    form['bonus_2_used'] = False
    
    # Labels de información
    form['lbl_clock'] = Label(
        x=1070,
        y=50,
        text=f'TIME LEFT: {form.get("level").get("level_timer")}',
        screen=form.get('screen'),
        font_path=var.FUENTE_ALAGARD
    )
    
    form['lbl_score'] = Label(
        x=150,
        y=50,
        text=f'SCORE: {form.get("jugador").get("puntaje_actual")}',
        screen=form.get('screen'),
        font_path=var.FUENTE_ALAGARD
    )
    
    # Inicializar iconos de wishes
    manejo_wishes.inicializar_wish_icons(form)
    
    # Botón principal de juego
    form['btn_play_hand'] = ButtonImage(
        x=1199,
        y=var.DIMENSION_PANTALLA[1] // 2 + 25,
        width=140,
        height=60,
        text='',
        screen=form.get('screen'),
        image_path='./assets_Dragon_Ball_Trading_Card_Game/img/buttons_image/btn_play_hand.png',
        font_size=30,
        on_click=play_hand,
        on_click_param=form
    )
    
    # Botones de wishes
    form['btn_wish_heal'] = ButtonImage(
        x=930,
        y=450,
        width=120,
        height=60,
        text='',
        screen=form.get('screen'),
        image_path='./assets_Dragon_Ball_Trading_Card_Game/img/buttons_image/heal.png',
        font_size=20,
        on_click=manejo_wishes.select_wish,
        on_click_param={'form': form, 'wish': 'HEAL'}
    )
    
    form['btn_wish_shield'] = ButtonImage(
        x=1060,
        y=450,
        width=120,
        height=60,
        text='',
        screen=form.get('screen'),
        image_path='./assets_Dragon_Ball_Trading_Card_Game/img/buttons_image/shield.png',
        font_size=20,
        on_click=manejo_wishes.select_wish,
        on_click_param={'form': form, 'wish': 'SHIELD'}
    )
    
    # Labels de stats del jugador
    form['lbl_jugador_hp'] = Label(
        x=195,
        y=515,
        text='HP: ---',
        screen=form.get('screen'),
        font_path=var.FUENTE_ALAGARD,
        color=var.COLOR_AMARILLO,
        font_size=16
    )
    
    form['lbl_jugador_atk'] = Label(
        x=195,
        y=535,
        text='ATK: ---',
        screen=form.get('screen'),
        font_path=var.FUENTE_ALAGARD,
        color=var.COLOR_AMARILLO,
        font_size=16
    )
    
    form['lbl_jugador_def'] = Label(
        x=195,
        y=555,
        text='DEF: ---',
        screen=form.get('screen'),
        font_path=var.FUENTE_ALAGARD,
        color=var.COLOR_AMARILLO,
        font_size=16
    )
    
    # Labels de stats del enemy
    form['lbl_enemy_hp'] = Label(
        x=195,
        y=184,
        text='HP: ---',
        screen=form.get('screen'),
        font_path=var.FUENTE_ALAGARD,
        color=var.COLOR_AMARILLO,
        font_size=16
    )
    
    form['lbl_enemy_atk'] = Label(
        x=195,
        y=204,
        text='ATK: ---',
        screen=form.get('screen'),
        font_path=var.FUENTE_ALAGARD,
        color=var.COLOR_AMARILLO,
        font_size=16
    )
    
    form['lbl_enemy_def'] = Label(
        x=195,
        y=224,
        text='DEF: ---',
        screen=form.get('screen'),
        font_path=var.FUENTE_ALAGARD,
        color=var.COLOR_AMARILLO,
        font_size=16
    )

    
    # Marcar que los labels de stats están inicializados
    form['stats_labels_inicializados'] = True
    
    # Lista de widgets para renderizar
    form['widgets_list'] = [
        form.get('lbl_clock'), 
        form.get('lbl_score'), 
        form.get('btn_wish_heal'), 
        form.get('btn_wish_shield'), 
        form.get('btn_play_hand'),
        form.get('lbl_jugador_hp'), 
        form.get('lbl_jugador_atk'), 
        form.get('lbl_jugador_def'),
        form.get('lbl_enemy_hp'), 
        form.get('lbl_enemy_atk'), 
        form.get('lbl_enemy_def')
    ]
    
    # Registrar formulario en el diccionario global
    base_form.forms_dict[dict_form_data.get('name')] = form
    
    # Configurar sistema de hover para botones
    form['botones_hover'] = {
        'btn_play_hand': False,
        'btn_heal': False,
        'btn_shield': False
    }
    
    # Configurar sonido de hover
    form['sonido_hover'] = None
    try:
        form['sonido_hover'] = pg.mixer.Sound('./assets_Dragon_Ball_Trading_Card_Game/audio/sounds/menu_select.wav')
    except:
        pass
    
    # Configurar rectángulos de colisión para hover
    form['botones_rects'] = {
        'btn_play_hand': pg.Rect(1199 - 70, var.DIMENSION_PANTALLA[1] // 2 + 25 - 30, 140, 60),
        'btn_heal': pg.Rect(930 - 60, 450 - 30, 120, 60),
        'btn_shield': pg.Rect(1060 - 60, 450 - 30, 120, 60)
    }
    
    return form


def play_hand(form):
    """
    Inicia la secuencia de batalla: entrada de cartas → espera 0.5s → choque → remoción
    
    Args:
        form: Diccionario con los datos del formulario
    """
    # Verificar si la batalla ya terminó
    if form.get('batalla_terminada', False):
        return
    
    # Verificar si hay una secuencia en progreso
    if form.get('secuencia_batalla_activa', False):
        return
    
    # Verificar si hay cartas disponibles
    if not form['level']['cartas_mazo_jugador'] or not form['level']['cartas_mazo_enemy']:
        return
    
    # Iniciar la secuencia de batalla
    manejo_cartas.iniciar_secuencia_batalla(form)




def actualizar_timer(dict_form_data: dict):
    """
    Actualiza el timer del nivel reduciendo un segundo cada 1000ms
    
    Args:
        dict_form_data: Diccionario con los datos del formulario
    """
    if dict_form_data.get('level').get('level_timer') > 0:
        tiempo_actual = pg.time.get_ticks()
        if tiempo_actual - dict_form_data.get('first_last_timer') > 1000:
            dict_form_data.get('level')['level_timer'] -= 1
            dict_form_data['first_last_timer'] = tiempo_actual


def events_handler(events_list: list[pg.event.Event]):
    """
    Maneja los eventos del formulario
    
    Args:
        events_list: Lista de eventos de pygame
    """
    for evento in events_list:
        if evento.type == pg.KEYDOWN:
            if evento.key == pg.K_ESCAPE:
                base_form.set_active('form_pause')
                base_form.stop_music()
                base_form.play_music(base_form.forms_dict['form_pause'])
                return

def draw(dict_form_data: dict):
    """
    Dibuja todos los elementos del formulario
    
    Args:
        dict_form_data: Diccionario con los datos del formulario
    """
    # Dibujar fondo
    fondo = pg.image.load('./assets_Dragon_Ball_Trading_Card_Game/img/background_cards.png')
    dict_form_data['screen'].blit(fondo, (0, 0))
    
    # Dibujar widgets base
    base_form.draw_widgets(dict_form_data)
    
    # Dibujar widgets de la lista (con condiciones para botones deshabilitados)
    for widget_index in range(len(dict_form_data.get('widgets_list'))):
        # Ocultar botones de wishes si ya fueron usados
        if ((widget_index == 2 and dict_form_data.get('jugador', {}).get('heal_usado', False)) or
            (widget_index == 3 and dict_form_data.get('jugador', {}).get('shield_usado', False))):
            continue
            
        # Ocultar botón PLAY HAND si la batalla terminó
        if widget_index == 4 and dict_form_data.get('batalla_terminada', False):
            continue
            
        dict_form_data.get('widgets_list')[widget_index].draw()
    
    # Dibujar labels de stats si están inicializados
    if dict_form_data.get('stats_labels_inicializados', False):
        dict_form_data['lbl_jugador_hp'].draw()
        dict_form_data['lbl_jugador_atk'].draw()
        dict_form_data['lbl_jugador_def'].draw()
        dict_form_data['lbl_enemy_hp'].draw()
        dict_form_data['lbl_enemy_atk'].draw()
        dict_form_data['lbl_enemy_def'].draw()
    
    # Dibujar iconos de wishes
    manejo_wishes.dibujar_wish_icons(dict_form_data)
    
    # Dibujar efectos de hover
    dibujar_efectos_hover(dict_form_data)
    
    # Dibujar cartas del nivel
    nivel_cartas.draw(dict_form_data.get('level'))


def update(dict_form_data: dict, cola_eventos: list[pg.event.Event]):
    """
    Actualiza todos los elementos del formulario
    
    Args:
        dict_form_data: Diccionario con los datos del formulario
        cola_eventos: Lista de eventos de pygame
    """
    # Actualizar textos de labels principales
    dict_form_data['lbl_clock'].update_text(
        f'TIME LEFT: {dict_form_data.get("level").get("level_timer")}', 
        (255, 0, 0)
    )
    dict_form_data['lbl_score'].update_text(
        f'SCORE: {dict_form_data.get("jugador").get("puntaje_actual")}', 
        (255, 0, 0)
    )
    
    # Actualizar stats en pantalla si están inicializados
    if dict_form_data.get('stats_labels_inicializados', False):
        actualizar_stats_pantalla(dict_form_data)
    
    # Actualizar animaciones de wishes
    manejo_wishes.update_wish_icons(dict_form_data, 16.67)
    
    # Actualizar secuencia de batalla
    delta_time = dict_form_data['clock'].get_time()
    manejo_cartas.actualizar_secuencia_batalla(dict_form_data, delta_time, actualizar_stats_pantalla)
    
    # Actualizar animaciones de cartas
    manejo_cartas.actualizar_animaciones_cartas(dict_form_data)
    
    # Manejar efectos de hover
    manejar_hover_botones(dict_form_data)
    
    # Actualizar widgets (con condiciones para botones deshabilitados)
    for widget_index in range(len(dict_form_data.get('widgets_list'))):
        # Saltear botones de wishes si ya fueron usados
        if ((widget_index == 2 and dict_form_data.get('jugador', {}).get('heal_usado', False)) or
            (widget_index == 3 and dict_form_data.get('jugador', {}).get('shield_usado', False))):
            continue
            
        # Saltear botón PLAY HAND si la batalla terminó
        if widget_index == 4 and dict_form_data.get('batalla_terminada', False):
            continue
            
        dict_form_data.get('widgets_list')[widget_index].update()
    
    # Actualizar nivel de cartas
    nivel_cartas.update(dict_form_data.get('level'), cola_eventos)
    
    # Actualizar reloj y timer
    dict_form_data['clock'].tick(var.FPS)
    actualizar_timer(dict_form_data)
    
    # Manejar eventos
    events_handler(cola_eventos)

def actualizar_stats_pantalla(form):
    """
    Actualiza los labels de stats del jugador y enemy en pantalla
    
    Args:
        form: Diccionario con los datos del formulario
    """
    if not form.get('stats_labels_inicializados', False):
        return
    
    jugador = form.get('jugador')
    enemy = form.get('enemy')
    
    if jugador and enemy:
        # Actualizar stats del jugador
        form['lbl_jugador_hp'].update_text(f'HP: {int(jugador["hp"])}', var.COLOR_AMARILLO)
        form['lbl_jugador_atk'].update_text(f'ATK: {int(jugador["atk"])}', var.COLOR_AMARILLO)
        form['lbl_jugador_def'].update_text(f'DEF: {int(jugador["def"])}', var.COLOR_AMARILLO)
        
        # Actualizar stats del enemy
        form['lbl_enemy_hp'].update_text(f'HP: {int(enemy["hp"])}', var.COLOR_AMARILLO)
        form['lbl_enemy_atk'].update_text(f'ATK: {int(enemy["atk"])}', var.COLOR_AMARILLO)
        form['lbl_enemy_def'].update_text(f'DEF: {int(enemy["def"])}', var.COLOR_AMARILLO)
        
        # Actualizar score
        form['lbl_score'].update_text(f'SCORE: {jugador["puntaje_actual"]}', (255, 0, 0))

def verificar_fin_juego(form):
    """
    Verifica si el juego ha terminado y maneja el ranking si corresponde
    
    Condiciones de terminación:
    - No quedan cartas en algún mazo
    - Algún jugador se quedó sin HP
    
    Args:
        form: Diccionario con los datos del formulario
    
    Returns:
        str|bool: "jugador_gano", "jugador_perdio" o False si no terminó
    """
    jugador = form.get('jugador')
    enemy = form.get('enemy')
    level = form.get('level')
    
    if not jugador or not enemy or not level:
        return False
    
    # Verificar si no quedan cartas
    sin_cartas_jugador = len(level.get('cartas_mazo_jugador', [])) == 0
    sin_cartas_enemy = len(level.get('cartas_mazo_enemy', [])) == 0
    
    # Normalizar HP negativo a 0
    if jugador['hp'] < 0:
        jugador['hp'] = 0
    if enemy['hp'] < 0:
        enemy['hp'] = 0
    
    # Verificar si alguien se quedó sin HP
    jugador_sin_hp = jugador['hp'] <= 0
    enemy_sin_hp = enemy['hp'] <= 0
    
    # Determinar si el juego terminó
    if sin_cartas_jugador or sin_cartas_enemy or jugador_sin_hp or enemy_sin_hp:
        # Determinar el ganador
        if jugador_sin_hp and not enemy_sin_hp:
            ganador_final = "enemy"
        elif enemy_sin_hp and not jugador_sin_hp:
            ganador_final = "jugador"
        elif jugador_sin_hp and enemy_sin_hp:
            # Ambos sin HP, gana el que tenga más puntaje
            ganador_final = "jugador" if jugador['puntaje_actual'] > 0 else "enemy"
        else:
            # Se terminaron las cartas, gana el que tenga más HP
            if jugador['hp'] > enemy['hp']:
                ganador_final = "jugador"
            elif enemy['hp'] > jugador['hp']:
                ganador_final = "enemy"
            else:
                # Empate en HP, gana el que tenga más puntaje
                ganador_final = "jugador" if jugador['puntaje_actual'] > 0 else "empate"
        
        # Retornar resultado
        if ganador_final == "jugador":
            return "jugador_gano"
        else:
            return "jugador_perdio"
    
    return False

def manejar_hover_botones(form_data: dict):
    """
    Maneja los efectos hover de los botones manualmente
    
    Args:
        form_data: Diccionario con los datos del formulario
    """
    mouse_pos = pg.mouse.get_pos()
    
    for nombre_boton, rect in form_data['botones_rects'].items():
        esta_hover = rect.collidepoint(mouse_pos)
        
        # Reproducir sonido cuando el hover cambia a True
        if esta_hover and not form_data['botones_hover'][nombre_boton]:
            if form_data['sonido_hover']:
                form_data['sonido_hover'].play()
        
        # Actualizar estado de hover
        form_data['botones_hover'][nombre_boton] = esta_hover


def dibujar_efectos_hover(form_data: dict):
    """
    Dibuja efectos visuales de hover sobre los botones
    
    Args:
        form_data: Diccionario con los datos del formulario
    """
    for nombre_boton, esta_hover in form_data['botones_hover'].items():
        if esta_hover:
            rect = form_data['botones_rects'][nombre_boton]
            
            # Crear superficie semi-transparente para el efecto
            superficie_hover = pg.Surface((rect.width + 10, rect.height + 10), pg.SRCALPHA)
            superficie_hover.fill((255, 255, 255, 50))
            
            # Dibujar superficie de hover
            form_data['screen'].blit(superficie_hover, (rect.x - 5, rect.y - 5))
            
            # Dibujar borde brillante
            pg.draw.rect(form_data['screen'], (255, 255, 255, 150), rect, 3)

def inicializar_stats_jugadores(form):
    """
    Inicializa las stats de jugador y enemy basadas en la sumatoria de sus mazos
    
    Args:
        form: Diccionario con los datos del formulario
    """
    manejo_cartas.inicializar_stats_jugadores(form)