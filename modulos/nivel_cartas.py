import pygame as pg
import modulos.variables as var
import modulos.auxiliar as aux
import random as rd
import modulos.carta as carta
import modulos.jugador as jugador_1
import modulos.enemy as enemy_mod

def inicializar_nivel_cartas(jugador: dict, pantalla: pg.Surface, nro_nivel: int, enemy: dict):

    nivel_data = {}
    nivel_data['nro_nivel'] = nro_nivel
    nivel_data['configs'] = {}
    nivel_data['cartas_mazo_juego'] = {}
    nivel_data['cartas_mazo_juego_final'] = []
    nivel_data['cartas_mazo_juego_final_vistas'] = []
    nivel_data['ruta_mazo'] = ''
    nivel_data['screen'] = pantalla
    nivel_data['jugador'] = jugador
    nivel_data['mazo_jugador'] = []
    nivel_data['mazo_enemy'] = []
    nivel_data['cartas_mazo_jugador_vistas'] = []
    nivel_data['cartas_mazo_enemy_vistas'] = []
    nivel_data['stats_mazo_atk'] = None
    nivel_data['stats_mazo_def'] = None
    nivel_data['stats_mazo_hp'] = None
    nivel_data['enemy'] = enemy

    nivel_data['juego_finalizado'] = False
    nivel_data['puntaje_guardado'] = False
    nivel_data['level_timer'] = var.timer
    nivel_data['ganador'] = None

    nivel_data['puntaje_nivel'] = 0
    nivel_data['data_cargada'] = False

    return nivel_data

def inicializar_data_nivel(nivel_data: dict):

    if nivel_data.get('mazos_inicializados', False):
        print("Mazos ya inicializados, omitiendo...")
        return

    cargar_configs_nivel(nivel_data)
    cargar_bd_cartas(nivel_data)

    jugador_1.asignar_mazo_jugador(nivel_data)
    enemy_mod.asignar_mazo_enemy(nivel_data)


    nivel_data['mazos_inicializados'] = True

def cargar_configs_nivel(nivel_data: dict):
    if not nivel_data.get('juego_finalizado') and not nivel_data.get('data_cargada'):
        configs_globales = aux.cargar_configs(var.RUTA_CONFIGS_JSON)
        nivel_data['configs'] = configs_globales

        nivel_data['rutas_mazos'] = nivel_data.get('configs').get('rutas_mazos')
        nivel_data['cantidades'] = nivel_data.get('configs').get('cantidades')
        nivel_data['coords_iniciales'] = nivel_data.get('configs').get('coordenadas').get('mazo_jugador')
        nivel_data['coords_finales'] = nivel_data.get('configs').get('coordenadas').get('mazo_enemy')


        if nivel_data['coords_iniciales']:
            coords_ini = nivel_data['coords_iniciales']
            nivel_data['coords_iniciales'] = (coords_ini.get('x'), coords_ini.get('y'))

        if nivel_data['coords_finales']:
            coords_fin = nivel_data['coords_finales']
            nivel_data['coords_finales'] = (coords_fin.get('x'), coords_fin.get('y'))

def cargar_bd_cartas(nivel_data: dict):
    if not nivel_data.get('juego_finalizado'):
        for nombre_mazo, ruta_mazo in nivel_data.get('rutas_mazos').items():
            bd = aux.generar_bd(ruta_mazo)
            dict_cartas = bd.get("cartas")

            lista_cartas = list(dict_cartas.values())[0]
            nivel_data['cartas_mazo_juego'][nombre_mazo] = lista_cartas

def eventos(nivel_data: dict, cola_eventos: list[pg.event.Event]):
    """
    Maneja los eventos de mouse para las cartas del nivel
    """
    for evento in cola_eventos:
        if evento.type == pg.MOUSEBUTTONDOWN:

            if nivel_data.get('cartas_mazo_jugador'):
                    carta_actual = nivel_data['cartas_mazo_jugador'][-1]
                    if not carta_actual.get('visible') and carta_actual.get('rect').collidepoint(evento.pos):

                        coords_finales = nivel_data.get('coords_finales')
                        if coords_finales is not None:
                            carta.asignar_coordenadas_carta(carta_actual, coords_finales)
                            carta.cambiar_visibilidad_carta(carta_actual)

                            carta_vista = nivel_data.get('cartas_mazo_jugador').pop()
                            nivel_data.get('cartas_mazo_jugador_vistas').append(carta_vista)

                            jugador_1.sumar_puntaje_carta_actual(nivel_data.get('jugador'), carta_vista)
                        else:
                            print("ERROR: coords_finales es None")

def tiempo_esta_terminado(nivel_data: dict):
    return nivel_data.get('level_timer') <= 0

def mazo_esta_vacio(nivel_data: dict):
    return len(nivel_data.get('cartas_mazo_jugador', [])) == 0 or len(nivel_data.get('cartas_mazo_enemy', [])) == 0

def check_juego_terminado(nivel_data: dict):
    if mazo_esta_vacio(nivel_data) or tiempo_esta_terminado(nivel_data):
        nivel_data['juego_finalizado'] = True





















def juego_terminado(nivel_data: dict):
    return nivel_data.get('juego_finalizado')

def reiniciar_nivel(nivel_cartas: dict, jugador: dict, pantalla: pg.Surface, nro_nivel: int, enemy: dict):
    jugador_1.set_puntaje_actual(jugador, 0)
    nivel_cartas = inicializar_nivel_cartas(jugador, pantalla, nro_nivel, enemy)
    return nivel_cartas

def draw(nivel_data: dict):

    for carta_jugador in nivel_data.get('cartas_mazo_jugador', []):
        carta.draw_carta(carta_jugador, nivel_data['screen'])


    for carta_enemy in nivel_data.get('cartas_mazo_enemy', []):
        carta.draw_carta(carta_enemy, nivel_data['screen'])


    for carta_jugador_vista in nivel_data.get('cartas_mazo_jugador_vistas', []):

        if (carta_jugador_vista.get('visible', False) or
            carta_jugador_vista.get('animando', False) or
            carta_jugador_vista.get('animando_volando', False) or
            carta_jugador_vista.get('animando_entrada', False)):
            carta.draw_carta(carta_jugador_vista, nivel_data['screen'])


    for carta_enemy_vista in nivel_data.get('cartas_mazo_enemy_vistas', []):

        if (carta_enemy_vista.get('visible', False) or
            carta_enemy_vista.get('animando', False) or
            carta_enemy_vista.get('animando_volando', False) or
            carta_enemy_vista.get('animando_entrada', False)):
            carta.draw_carta(carta_enemy_vista, nivel_data['screen'])

def update(nivel_data: dict, cola_eventos: list[pg.event.Event]):
    eventos(nivel_data, cola_eventos)
    check_juego_terminado(nivel_data)
    if juego_terminado(nivel_data) and not nivel_data.get('puntaje_guardado'):
        jugador_1.actualizar_puntaje_total(nivel_data.get('jugador'))
        nivel_data['puntaje_guardado'] = True

