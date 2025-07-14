import modulos.variables as var
import pygame as pg
import sys
import modulos.forms.form_manager as form_manager
import modulos.jugador as jugador_1
import modulos.enemy as enemy


def pythonisa():

    pg.init()
    pg.mixer.init()

    pg.display.set_caption(var.TITULO_JUEGO)
    pantalla = pg.display.set_mode(var.DIMENSION_PANTALLA)

    corriendo = True
    reloj = pg.time.Clock()

    datos_juego = {
    'jugador': jugador_1.inicializar_jugador(),
    'enemy': enemy.inicializar_enemy(),

    'turno_actual': 0,

    'cartas_restantes': {
        'jugador': 0,
        'enemy': 0
    },

    'tiempo_restante': 60,
    'resultado': None,
    "comodin_activo": None,
    "ranking": []
    }


    f_manager = form_manager.create_form_manager(pantalla, datos_juego)


    while corriendo:

        event_list = pg.event.get()
        reloj.tick(var.FPS)

        for event in event_list:
            if event.type == pg.QUIT:
                corriendo = False

        pantalla.fill((0, 0, 0))
        form_manager.update(f_manager, event_list)

        pg.display.flip()
    pg.quit()
    sys.exit()
