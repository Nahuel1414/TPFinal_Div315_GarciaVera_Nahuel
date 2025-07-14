import pygame as pg
import modulos.variables as var
import modulos.forms.form_main_menu as form_main_menu
import modulos.forms.form_options as form_options
import modulos.forms.form_ranking as form_ranking
import modulos.forms.form_start_level as form_start_level
import modulos.forms.form_enter_name as form_enter_name
import modulos.forms.form_pause as form_pause
import modulos.forms.form_wish as form_wish
import modulos.forms.form_defeat as form_defeat

def create_form_manager(screen: pg.Surface, datos_juego: dict):
    """Esta funcion crea el form manager y maneja los diferentes formularios del juego.

    Args:
        screen (pg.Surface): pantalla de pygame.
        datos_juego (dict): diccionario con todos los datos del juego.

    Returns:
        form: retorna el diccionario que contiene la info del form manager.
    """
    form = {}

    form['main_screen'] = screen
    form['datos_juego'] = datos_juego
    form['form_list'] = []

    form['jugador'] = datos_juego.get('jugador')
    form['enemy'] = datos_juego.get('enemy')

    form['form_list'] = [
        form_main_menu.init_form_main_menu(
            dict_form_data={
                "name":'form_main_menu',
                "screen":form.get('main_screen'),
                "active":True,
                "coords":(0,0),
                "stage_number":1,
                "music_path":var.RUTA_MUSICA,
                "background_path": './assets_Dragon_Ball_Trading_Card_Game/img/moon_background.png',
                "screen_dimentions": var.DIMENSION_PANTALLA,
                'botones': {
                    'start': './assets_Dragon_Ball_Trading_Card_Game/icons_main_menu/start.png',
                    'options': './assets_Dragon_Ball_Trading_Card_Game/icons_main_menu/options.png',
                    'ranking': './assets_Dragon_Ball_Trading_Card_Game/icons_main_menu/ranking.png',
                    'salir': './assets_Dragon_Ball_Trading_Card_Game/icons_main_menu/exit.png'
                },
                'sonido_botones': './assets_Dragon_Ball_Trading_Card_Game/audio/sounds/menu_select.wav'
            }
        ),

        form_options.init_form_options(
            dict_form_data={
                "name":'form_options',
                "screen":form.get('main_screen'),
                "active":True,
                "coords":(0,0),
                "stage_number":1,
                "music_path":var.RUTA_MUSICA,
                "background_path": './assets_Dragon_Ball_Trading_Card_Game/img/space.png',
                "screen_dimentions": var.DIMENSION_PANTALLA,
                'botones': {
                    'volver': './assets_Dragon_Ball_Trading_Card_Game/icons_main_menu/btn_volver.png'
                },
                'sonido_botones': './assets_Dragon_Ball_Trading_Card_Game/audio/sounds/menu_select.wav'
            }
        ),

        form_ranking.init_form_ranking(
            dict_form_data={
                "name":'form_ranking',
                "screen":form.get('main_screen'),
                "active":True,
                "coords":(0,0),
                "stage_number":1,
                "music_path":var.RUTA_MUSICA,
                "background_path": './assets_Dragon_Ball_Trading_Card_Game/img/moon_background.png',
                "screen_dimentions": var.DIMENSION_PANTALLA,
                'botones': {
                    'volver': './assets_Dragon_Ball_Trading_Card_Game/icons_main_menu/btn_volver.png'
                },
                'sonido_botones': './assets_Dragon_Ball_Trading_Card_Game/audio/sounds/menu_select.wav'
            }, jugador=form.get('jugador')
        ),

        form_start_level.init_form_start_level(
            dict_form_data={
                "name":'form_start_level',
                "screen":form.get('main_screen'),
                "active":True,
                "coords":(0,0),
                "stage_number":1,
                "music_path":var.RUTA_MUSICA,
                "background_path": './assets_Dragon_Ball_Trading_Card_Game/img/background_cards.png',
                "screen_dimentions": var.DIMENSION_PANTALLA,
            }, jugador=form.get('jugador'), enemy=form.get('enemy')
        ),

        form_enter_name.init_form_enter_name(
            dict_form_data={
                "name":'form_enter_name',
                "screen":form.get('main_screen'),
                "active":True,
                "coords":(0,0),
                "stage_number":1,
                "music_path":var.RUTA_MUSICA,
                "background_path": './assets_Dragon_Ball_Trading_Card_Game/img/background_cards.png',
                "screen_dimentions": var.DIMENSION_PANTALLA,
            }, jugador=form.get('jugador')
        ),

        form_pause.init_form_pause(
            dict_form_data={
                "name":'form_pause',
                "screen":form.get('main_screen'),
                "active":True,
                "coords":(0,0),
                "stage_number":1,
                "music_path":var.RUTA_MUSICA,
                "background_path": './assets_Dragon_Ball_Trading_Card_Game/img/space.png',
                "screen_dimentions": var.DIMENSION_PANTALLA,
            }
        ),

        form_wish.init_form_wish(
            dict_form_data={
                "name":'form_wish',
                "screen":form.get('main_screen'),
                "active":True,
                "coords":(0,0),
                "stage_number":1,
                "music_path":var.RUTA_MUSICA,
                "background_path": './assets_Dragon_Ball_Trading_Card_Game/img/space.png',
                "screen_dimentions": var.DIMENSION_PANTALLA,
            }, jugador=form.get('jugador')
        ),

        form_defeat.init_form_defeat(
            dict_form_data={
                "name":'form_defeat',
                "screen":form.get('main_screen'),
                "active":True,
                "coords":(0,0),
                "stage_number":1,
                "music_path":var.RUTA_MUSICA,
                "background_path": './assets_Dragon_Ball_Trading_Card_Game/img/space.png',
                "screen_dimentions": var.DIMENSION_PANTALLA,
            }, jugador=form.get('jugador')
        )
    ]
    return form

def forms_update(form_manager: dict, lista_eventos: pg.event.Event):
    """Verifica si alguno de los formularios esta activo. En caso de estar activo, lo dibuja y lo actualiza.

    Args:
        form_manager (dict): diccionario que maneja los forms y sus datos.
        lista_eventos (pg.event.Event): lista de eventos de pygame.
    """

    if form_manager.get('form_list')[0].get('active'):
        form_main_menu.update(form_manager.get('form_list')[0])
        form_main_menu.draw(form_manager.get('form_list')[0])


    elif form_manager.get('form_list')[1].get('active'):
        form_main_menu.update(form_manager.get('form_list')[1])
        form_main_menu.draw(form_manager.get('form_list')[1])


    elif form_manager.get('form_list')[2].get('active'):
        form_ranking.update(form_manager.get('form_list')[2])
        form_ranking.draw(form_manager.get('form_list')[2])


    elif form_manager.get('form_list')[3].get('active'):
        form_start_level.update(form_manager.get('form_list')[3], lista_eventos)
        form_start_level.draw(form_manager.get('form_list')[3])


    elif form_manager.get('form_list')[4].get('active'):
        form_enter_name.update(form_manager.get('form_list')[4], lista_eventos)
        form_enter_name.draw(form_manager.get('form_list')[4])


    elif form_manager.get('form_list')[5].get('active'):
        form_pause.update(form_manager.get('form_list')[5])
        form_pause.draw(form_manager.get('form_list')[5])


    elif form_manager.get('form_list')[6].get('active'):
        form_wish.update(form_manager.get('form_list')[6])
        form_wish.draw(form_manager.get('form_list')[6])


    elif form_manager.get('form_list')[7].get('active'):
        form_defeat.update(form_manager.get('form_list')[7], lista_eventos)
        form_defeat.draw(form_manager.get('form_list')[7])

def update(form_manager: dict, lista_eventos: pg.event.Event):
    """Llama a la funcion forms_update, actualiza y dibuja el formulario activo en el juego.

    Args:
        form_manager (dict): diccionario que maneja los forms y sus datos.
        lista_eventos (pg.event.Event): lista de eventos de pygame.
    """
    forms_update(form_manager, lista_eventos)
