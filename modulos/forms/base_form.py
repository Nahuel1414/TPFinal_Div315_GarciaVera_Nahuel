import pygame as pg
import modulos.variables as var

forms_dict = {}

def create_base_form(dict_form_data: dict) -> dict:
    """Creamos el formulario base.

    Args:
        dict_form_data (dict): recibe un diccionario con los datos de un form.

    Returns:
        dict: devuelve el diccionario con sus respectivas claves.
    """
    form = {}
    form['name'] = dict_form_data.get('name')
    form['screen'] = dict_form_data.get('screen')
    form['active'] = dict_form_data.get('active')
    form['x_coord'] = dict_form_data.get('coords')[0]
    form['y_coord'] = dict_form_data.get('coords')[1]
    form['level_number'] = dict_form_data.get('stage_number')
    form['music_path'] = dict_form_data.get('music_path')
    form['surface'] = pg.image.load(dict_form_data.get('background_path')).convert_alpha()
    form['surface'] = pg.transform.scale(form.get('surface'), dict_form_data.get('screen_dimentions'))

    form['rect'] = form.get('surface').get_rect()
    form['rect'].x = dict_form_data.get('coords')[0]
    form['rect'].y = dict_form_data.get('coords')[1]
    return form

def play_music(form_dict: dict):
    pg.mixer.music.load(form_dict.get('music_path'))
    pg.mixer.music.set_volume(0.4)
    pg.mixer.music.play(loops=1, fade_ms=400)

def stop_music():
    pg.mixer.music.stop()

def set_active(name: str):
    """Activa el formulario adecuado

    Args:
        name (str): nombre del formulario
    """
    for form in forms_dict.values():
        form['active'] = False
    forms_dict[name]['active'] = True

def update_widgets(form_data: dict):
    """Actualizamos los widgets

    Args:
        form_data (dict): Recibe el diccionario con los datos.
    """
    for widget in form_data.get('widgets_list'):
        widget.update()

def draw_widgets(form_data: dict):
    """Dibujamos los widgets.

    Args:
        form_data (dict): Recibe el diccionario con los datos.
    """
    for widget in form_data.get('widgets_list'):
        widget.draw()

def draw(form_data: dict):
    """Dibujamos la pantalla

    Args:
        form_data (dict): Recibe el diccionario con los datos.
    """
    form_data['screen'].blit(form_data.get('surface'), form_data.get('rect'))
    draw_widgets(form_data)

def update(form_data: dict):
    """Dibujamos la pantalla

    Args:
        form_data (dict): Recibe el diccionario con los datos.
    """
    update_widgets(form_data)
