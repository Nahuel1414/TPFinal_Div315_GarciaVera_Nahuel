import modulos.forms.base_form as base_form
import modulos.variables as var
import modulos.auxiliar as aux
import modulos.jugador as jugador_mod
import pygame as pg
from utn_fra.pygame_widgets import (
    Button, Label, TextBox
)

def init_form_wish(dict_form_data: dict, jugador: dict):
    form = base_form.create_base_form(dict_form_data)
    form['jugador'] = jugador
    form['wish_info'] = ''

    form['title'] = Label(
        x= var.DIMENSION_PANTALLA[0] // 2,
        y= var.DIMENSION_PANTALLA[1] // 2 - 250,
        text= var.TITULO_JUEGO,
        screen= form.get('screen'),
        font_path= var.FUENTE_ANCIENT,
        font_size= 75
    )

    form['subtitle'] = Label(
        x= var.DIMENSION_PANTALLA[0] // 2,
        y= var.DIMENSION_PANTALLA[1] // 2 - 175,
        text= 'SELECCIONA UN WISH',
        screen= form.get('screen'),
        font_path= var.FUENTE_ANCIENT,
        font_size= 50,
        color= var.COLOR_NARANJA
    )

    form['btn_select'] = Button(
        x= var.DIMENSION_PANTALLA[0] // 2 - 200,
        y= var.DIMENSION_PANTALLA[1] // 2 + 50,
        text= form.get('wish_info'),
        screen= form.get('screen'),
        font_path= var.FUENTE_ANCIENT,
        on_click= click_select_wish,
        on_click_param= form
    )

    form['btn_back'] = Button(
        x= var.DIMENSION_PANTALLA[0] // 2 + 200,
        y= var.DIMENSION_PANTALLA[1] // 2 + 50,
        text= 'CANCELAR',
        screen= form.get('screen'),
        font_path= var.FUENTE_ANCIENT,
        on_click= click_change_form,
        on_click_param= 'form_start_level'
    )

    form['widgets_list'] = [
        form.get('title'), form.get('subtitle'), form.get('btn_select'), form.get('btn_back')
    ]

    base_form.forms_dict[dict_form_data.get('name')] = form

    return form

def click_change_form(parametro: str):
    base_form.stop_music()
    base_form.play_music(base_form.forms_dict[parametro])
    base_form.set_active(parametro)

def click_select_wish(form_data: dict):
    option = form_data.get('wish_info')
    jugador = form_data.get('jugador')

    print(f"=== USANDO COMODÍN: {option} ===")

    match option:
        case 'HEAL':
            if not jugador.get('heal_usado', False):

                import modulos.batalla as batalla
                exito = batalla.usar_comodin_heal(jugador)
                if exito:
                    print(f"HEAL usado: HP restaurado a {jugador['hp']}")
                else:
                    print("ERROR: No se pudo usar HEAL")
            else:
                print("HEAL ya fue usado")

        case 'SHIELD':
            if not jugador.get('shield_usado', False):

                import modulos.batalla as batalla
                exito = batalla.usar_comodin_shield(jugador)
                if exito:
                    print(f"SHIELD activado")
                else:
                    print("ERROR: No se pudo usar SHIELD")
            else:
                print("SHIELD ya fue usado")

    print(f"Estado jugador - HP: {jugador['hp']}, HEAL usado: {jugador.get('heal_usado')}, SHIELD usado: {jugador.get('shield_usado')}, SHIELD activo: {jugador.get('shield_activo')}")


    pg.time.wait(1000)
    click_change_form('form_start_level')

def update_button_wish(form_data: dict, new_text: str):
    form_data['wish_info'] = new_text

    form_data.get('widgets_list')[2].update_text(form_data.get('wish_info'), var.COLOR_NEGRO)

def draw(form_data: dict):
    base_form.draw(form_data)

def update(form_data: dict):
    base_form.update(form_data)
