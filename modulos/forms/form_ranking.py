import pygame as pg
import modulos.forms.base_form as base_form
import modulos.variables as var
import modulos.auxiliar as aux
from utn_fra.pygame_widgets import (
    Button, Label, ButtonImage
)

def init_form_ranking(dict_form_data: dict, jugador: dict):
    form = base_form.create_base_form(dict_form_data)

    form['jugador'] = jugador

    form['ranking_screen'] = []
    form['ranking_list'] = []

    form['lbl_titulo'] = Label(
        x=var.DIMENSION_PANTALLA[0]//2,
        y=var.DIMENSION_PANTALLA[1]//2 - 250,
        text='DRAGON BALL Z TCG',
        screen=form.get('screen'),
        font_path=var.FUENTE_ALAGARD,
        font_size=70)

    form['lbl_subtitulo'] = Label(
        x=var.DIMENSION_PANTALLA[0]//2,
        y=var.DIMENSION_PANTALLA[1]//2 - 175,
        text='TOP 10 RANKING',
        screen=form.get('screen'),
        font_path=var.FUENTE_ALAGARD,
        font_size=50)

    form['btn_volver'] = ButtonImage(
        x=993,
        y=580,
        text= '',
        width=126,
        height=33,
        screen= form.get('screen'),
        image_path= dict_form_data.get('botones').get('volver'),
        font_size= 30,
        on_click= click_volver,
        on_click_param='form_main_menu')

    form['data_loaded'] = False

    form['widgets_list'] = [form.get('lbl_titulo'), form.get('lbl_subtitulo'), form.get('btn_volver')]

    base_form.forms_dict[dict_form_data.get('name')] = form

    return form


def click_volver(parametro: str):
    base_form.stop_music()
    base_form.play_music(base_form.forms_dict[parametro])
    base_form.set_active(parametro)
    base_form.forms_dict['form_ranking']['data_loaded'] = False

def init_ranking(form_data: dict):
    """
    Crea los labels de números, nombres y puntuaciones para mostrar el ranking
    """
    form_data['ranking_screen'] = []
    matriz = form_data.get('ranking_list')

    if not matriz:
        return


    for indice_fila in range(len(matriz)):
        fila = matriz[indice_fila]


        form_data['ranking_screen'].append(
            Label(
                x= var.DIMENSION_PANTALLA[0]//2 - 220,
                y= var.DIMENSION_PANTALLA[1]//2.9+indice_fila*31,
                text=f'{indice_fila + 1}',
                screen= form_data.get('screen'),
                font_path= var.FUENTE_ALAGARD,
                color= var.COLOR_ROJO,
                font_size= 40
            )
        )


        form_data['ranking_screen'].append(
            Label(
                x= var.DIMENSION_PANTALLA[0]//2,
                y= var.DIMENSION_PANTALLA[1]//2.9+indice_fila*31,
                text=f'{fila[0]}',
                screen= form_data.get('screen'),
                font_path= var.FUENTE_ALAGARD,
                color= var.COLOR_ROJO,
                font_size= 40
            )
        )


        form_data['ranking_screen'].append(
            Label(
                x= var.DIMENSION_PANTALLA[0]//2 + 220,
                y= var.DIMENSION_PANTALLA[1]//2.9+indice_fila*31,
                text=f'{fila[1]}',
                screen= form_data.get('screen'),
                font_path= var.FUENTE_ALAGARD,
                color= var.COLOR_ROJO,
                font_size= 40
            )
        )


    form_data['widgets_list'].extend(form_data['ranking_screen'])

def inicializar_ranking(form_data: dict):
    """
    Carga los datos del ranking desde el archivo CSV y inicializa la visualización
    """

    ranking_completo = aux.cargar_ranking()
    form_data['ranking_list'] = ranking_completo[:10]


    form_data['widgets_list'] = [form_data.get('lbl_titulo'), form_data.get('lbl_subtitulo'), form_data.get('btn_volver')]


    init_ranking(form_data)

def draw(form_data: dict):
    """
    Dibuja el formulario de ranking en pantalla
    """
    base_form.draw(form_data)

def update(form_data: dict):
    """
    Actualiza el formulario de ranking y carga los datos si es necesario
    """

    if form_data.get('active') and not form_data.get('data_loaded'):
        inicializar_ranking(form_data)
        form_data['data_loaded'] = True


    base_form.update(form_data)
