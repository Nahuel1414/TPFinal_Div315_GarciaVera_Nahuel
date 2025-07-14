import modulos.forms.base_form as base_form
import modulos.variables as var
from utn_fra.pygame_widgets import (
    Button, Label
)

def init_form_defeat(dict_form_data: dict, jugador: dict):
    form = base_form.create_base_form(dict_form_data)

    form['jugador'] = jugador

    form['title'] = Label(
        x= var.DIMENSION_PANTALLA[0] // 2,
        y= var.DIMENSION_PANTALLA[1] // 2 - 200,
        text= var.TITULO_JUEGO,
        screen= form.get('screen'),
        font_path= var.FUENTE_ANCIENT,
        font_size= 75
    )

    form['title_2'] = Label(
        x= var.DIMENSION_PANTALLA[0] // 2,
        y= var.DIMENSION_PANTALLA[1] // 2 - 150,
        text= '¡PERDISTE!',
        screen= form.get('screen'),
        font_path= var.FUENTE_ANCIENT,
        font_size= 50,
        color= (255, 0, 0)
    )

    form['subtitle'] = Label(
        x= var.DIMENSION_PANTALLA[0] // 2,
        y= var.DIMENSION_PANTALLA[1] // 2 - 90,
        text= 'El enemy ha ganado la batalla',
        screen= form.get('screen'),
        font_path= var.FUENTE_ANCIENT,
        font_size= 30,
        color= var.COLOR_CIAN
    )

    form['subtitle_score'] = Label(
        x= var.DIMENSION_PANTALLA[0] // 2,
        y= var.DIMENSION_PANTALLA[1] // 2 - 20,
        text= f'Puntaje final: {jugador.get("puntaje_actual", 0)}',
        screen= form.get('screen'),
        font_path= var.FUENTE_ANCIENT,
        font_size= 30,
        color= var.COLOR_NARANJA
    )

    form['btn_return_menu'] = Button(
        x= var.DIMENSION_PANTALLA[0] // 2,
        y= var.DIMENSION_PANTALLA[1] // 2 + 50,
        text= 'VOLVER AL MENÚ',
        screen= form.get('screen'),
        font_path= var.FUENTE_ANCIENT,
        font_size= 40,
        on_click= click_return_menu,
        on_click_param= 'form_main_menu'
    )

    form['widgets_list'] = [
        form.get('title'), form.get('title_2'), form.get('subtitle'),
        form.get('subtitle_score'), form.get('btn_return_menu')
    ]

    base_form.forms_dict[dict_form_data.get('name')] = form

    return form

def click_return_menu(parametro: str):
    """Regresa al menú principal"""
    base_form.stop_music()
    base_form.play_music(base_form.forms_dict[parametro])
    base_form.set_active(parametro)

def draw(form_dict: dict):
    base_form.draw(form_dict)

def update(form_dict: dict, event_list: list):
    base_form.update(form_dict)
