import pygame as pg
import sys
import modulos.forms.base_form as base_form
import modulos.variables as var
import modulos.nivel_cartas as nivel_cartas
from utn_fra.pygame_widgets import (
    Button, Label, ButtonImageSound
)

def init_form_main_menu(dict_form_data: dict):
    """Inicializa el formulario del main menu

    Args:
        dict_form_data (dict): Recibe un diccionario

    Returns:
        dict: Devuelve el formulario con sus respectivos labels y botones.
    """
    form = base_form.create_base_form(dict_form_data)


    form['botones_hover'] = {
        'btn_start': False,
        'btn_options': False,
        'btn_ranking': False,
        'btn_salir': False
    }


    form['sonido_hover'] = None
    try:
        form['sonido_hover'] = pg.mixer.Sound('./assets_Dragon_Ball_Trading_Card_Game/audio/sounds/menu_select.wav')
    except:
        pass

    form['lbl_titulo'] = Label(
        x= var.DIMENSION_PANTALLA[0]//2,
        y=100,
        text= var.TITULO_JUEGO,
        screen=form.get('screen'),
        font_path=var.FUENTE_ANCIENT,
        font_size= 85)

    form['lbl_subtitulo'] = Label(
        x= var.DIMENSION_PANTALLA[0]//2,
        y=150,
        text= var.SUBTITULO_JUEGO,
        screen=form.get('screen'),
        font_path=var.FUENTE_ANCIENT,
        font_size= 60)


    form['botones_rects'] = {
        'btn_start': pg.Rect(var.DIMENSION_PANTALLA[0]//2 + 200 - 128, 260 - 33, 256, 66),
        'btn_options': pg.Rect(var.DIMENSION_PANTALLA[0]//2 + 200 - 128, 340 - 33, 256, 66),
        'btn_ranking': pg.Rect(var.DIMENSION_PANTALLA[0]//2 + 200 - 128, 420 - 33, 256, 66),
        'btn_salir': pg.Rect(var.DIMENSION_PANTALLA[0]//2 + 200 - 128, 500 - 33, 256, 66)
    }

    form['btn_start'] = ButtonImageSound(
        x=var.DIMENSION_PANTALLA[0]//2 + 200,
        y=260,
        width=256,
        height=66,
        text= '',
        screen= form.get('screen'),
        image_path= dict_form_data.get('botones').get('start'),
        sound_path= dict_form_data.get('sonido_botones'),
        font_size= 30,
        on_click= cambiar_formulario_on_click,
        on_click_param='form_start_level')

    form['btn_options'] = ButtonImageSound(
        x=var.DIMENSION_PANTALLA[0]//2 + 200,
        y=340,
        width=256,
        height=66,
        text= '',
        screen= form.get('screen'),
        image_path= dict_form_data.get('botones').get('options'),
        sound_path= dict_form_data.get('sonido_botones'),
        font_size= 30,
        on_click= cambiar_formulario_on_click,
        on_click_param='form_options')

    form['btn_ranking'] = ButtonImageSound(
        x=var.DIMENSION_PANTALLA[0]//2 + 200,
        y=420,
        width=256,
        height=66,
        text= '',
        screen= form.get('screen'),
        image_path= dict_form_data.get('botones').get('ranking'),
        sound_path= dict_form_data.get('sonido_botones'),
        font_size= 30,
        on_click= cambiar_formulario_on_click,
        on_click_param='form_ranking')

    form['btn_salir'] = ButtonImageSound(
        x=var.DIMENSION_PANTALLA[0]//2 + 200,
        y=500,
        width=256,
        height=66,
        text= 'EXIT',
        screen= form.get('screen'),
        image_path= dict_form_data.get('botones').get('salir'),
        sound_path= dict_form_data.get('sonido_botones'),
        font_size= 30,
        on_click= click_salir,
        on_click_param='Boton salir')

    form['widgets_list'] = [
        form.get('lbl_titulo'), form.get('lbl_subtitulo'), form.get('btn_start'), form.get('btn_options'), form.get('btn_ranking'), form.get('btn_salir')
    ]

    base_form.forms_dict[dict_form_data.get('name')] = form

    return form


def click_start(parametro: str):
    """Función para manejar el botón de start"""
    pass

def cambiar_formulario_on_click(parametro: str):
    """Cambiar formulario al hacer clic"""
    if parametro == 'form_start_level':
        form_start_level = base_form.forms_dict[parametro]


        form_start_level['batalla_terminada'] = False
        form_start_level['bonus_1_used'] = False
        form_start_level['bonus_2_used'] = False


        form_start_level['level'] = nivel_cartas.reiniciar_nivel(
            form_start_level.get('level'), form_start_level.get('jugador'),
            form_start_level.get('screen'), form_start_level.get('level_number'), form_start_level.get('enemy'))

        nivel_cartas.inicializar_data_nivel(form_start_level.get('level'))


        jugador = form_start_level.get('jugador')
        enemy = form_start_level.get('enemy')


        if jugador:
            jugador['heal_usado'] = False
            jugador['shield_usado'] = False
            jugador['puntaje_actual'] = 0


        import modulos.forms.form_start_level as form_start_level_mod
        form_start_level_mod.inicializar_stats_jugadores(form_start_level)
        form_start_level['stats_labels_inicializados'] = True
        form_start_level_mod.actualizar_stats_pantalla(form_start_level)

    base_form.set_active(parametro)
    base_form.stop_music()
    base_form.play_music(base_form.forms_dict[parametro])

def click_salir(parametro: str):
    """Función para manejar el botón de salir"""
    pass
    sys.exit()

def draw(form_data: dict):
    base_form.draw(form_data)

    dibujar_efectos_hover(form_data)


def update(form_data: dict):

    manejar_hover_botones(form_data)
    base_form.update(form_data)

def manejar_hover_botones(form_data: dict):
    """Maneja los efectos de hover en los botones del menú principal"""
    mouse_pos = pg.mouse.get_pos()

    for boton_nombre, rect in form_data['botones_rects'].items():

        mouse_sobre_boton = rect.collidepoint(mouse_pos)


        if mouse_sobre_boton and not form_data['botones_hover'][boton_nombre]:
            form_data['botones_hover'][boton_nombre] = True
            if form_data['sonido_hover']:
                form_data['sonido_hover'].play()


        elif not mouse_sobre_boton and form_data['botones_hover'][boton_nombre]:
            form_data['botones_hover'][boton_nombre] = False

def dibujar_efectos_hover(form_data: dict):
    """Dibuja efectos visuales de hover en los botones"""
    for boton_nombre, hover_activo in form_data['botones_hover'].items():
        if hover_activo:
            rect = form_data['botones_rects'][boton_nombre]


            superficie_hover = pg.Surface((rect.width + 10, rect.height + 10))
            superficie_hover.set_alpha(100)
            superficie_hover.fill((255, 255, 255))


            form_data['screen'].blit(superficie_hover, (rect.x - 5, rect.y - 5))


            pg.draw.rect(form_data['screen'], (255, 255, 0), rect, 3)
