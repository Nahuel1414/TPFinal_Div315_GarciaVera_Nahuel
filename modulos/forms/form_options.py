import modulos.forms.base_form as base_form
import modulos.variables as var
from utn_fra.pygame_widgets import (
    Label, Button
)

def init_form_options(dict_form_data: dict):
    """Inicializa el formulario de opciones y crea los botones necesarios

    Args:
        dict_form_data (dict): Recibe un diccionario con la data del formulario.

    Returns:
        dict: Retorna el formulario cargado.
    """
    form = base_form.create_base_form(dict_form_data)

    form['btn_back'] = Button(
        x= var.DIMENSION_PANTALLA[0] // 2,
        y= var.DIMENSION_PANTALLA[1] // 2 + 175,
        text= 'VOLVER AL MENU',
        screen= form.get('screen'),
        font_path= var.FUENTE_ANCIENT,
        on_click= click_change_form,
        on_click_param= 'form_main_menu'
    )













    form['widgets_list'] = [
        form.get('btn_back')
    ]

    base_form.forms_dict[dict_form_data.get('name')] = form

    return form

def click_change_form(parametro: str):
    base_form.stop_music()
    base_form.play_music(base_form.forms_dict[parametro])
    base_form.set_active(parametro)

def draw(form_data: dict):
    base_form.draw(form_data)

def update(form_data: dict):
    base_form.update(form_data)
