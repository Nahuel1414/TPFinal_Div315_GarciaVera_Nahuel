import modulos.carta as carta
import random as rd

def asignar_mazo_jugador(nivel_data: dict):
    mazo_keys = list(nivel_data['cartas_mazo_juego'].keys())

    mazos_validos = [mazo for mazo in mazo_keys if mazo != "./assets_Dragon_Ball_Trading_Card_Game/img/decks"]

    if not mazos_validos:
        return


    mazo_jugador = rd.choice(mazos_validos)


    nivel_data['mazos_disponibles'] = mazos_validos
    nivel_data['mazo_jugador_seleccionado'] = mazo_jugador


    coords_mazo = nivel_data['configs']['coordenadas']['mazo_jugador']
    coords_jugada = nivel_data['configs']['coordenadas']['jugada_jugador']

    nivel_data['cartas_mazo_jugador'] = []
    cartas_mazo = nivel_data['cartas_mazo_juego'][mazo_jugador]


    for carta_data in cartas_mazo:
        carta_mazo = carta.inicializar_carta(carta_data, coords_mazo)
        carta_mazo['visible'] = False
        nivel_data['cartas_mazo_jugador'].append(carta_mazo)

def inicializar_jugador(mazo=None):
    jugador_actual = {}

    jugador_actual['puntaje_actual'] = 0
    jugador_actual['puntaje_total'] = 0
    jugador_actual['nombre'] = 'Player'
    jugador_actual['heal_usado'] = False
    jugador_actual['shield_usado'] = False
    jugador_actual['shield_activo'] = False

    if mazo:
        hp, atk, df = calcular_stats_mazo(mazo)
        jugador_actual['hp'] = hp
        jugador_actual['atk'] = atk
        jugador_actual['def'] = df
        jugador_actual['hp_inicial'] = hp
    else:
        jugador_actual['hp'] = 100
        jugador_actual['atk'] = 10
        jugador_actual['def'] = 10
        jugador_actual['hp_inicial'] = 100

    return jugador_actual

def calcular_stats_mazo(mazo):
    hp_total = 0
    atk_total = 0
    def_total = 0

    for card in mazo:
        hp_total += card.get('hp', 0)
        atk_total += card.get('atk', 0)
        def_total += card.get('def', 0)
    return hp_total, atk_total, def_total

def usar_heal(jugador_actual: dict):
    if not jugador_actual.get('heal_usado'):
        jugador_actual['hp'] = jugador_actual.get('hp_inicial', jugador_actual['hp'])
        jugador_actual['heal_usado'] = True

def usar_shield(jugador_actual: dict):
    if not jugador_actual.get('shield_usado'):
        jugador_actual['shield_activo'] = True
        jugador_actual['shield_usado'] = True

def desactivar_shield(jugador_actual: dict):
    jugador_actual['shield_activo'] = False

def perdida_stats_jugador(jugador_actual: dict, carta_enemy: dict):
    bonus = carta_enemy.get('bonus', 1)
    jugador_actual['hp'] -= carta_enemy.get('atk') * bonus
    jugador_actual['atk'] -= carta_enemy.get('atk') * bonus
    jugador_actual['def'] -= carta_enemy.get('def') * bonus

    if jugador_actual['hp'] < 0:
        jugador_actual['hp'] = 0
    if jugador_actual['atk'] < 0:
        jugador_actual['atk'] = 0
    if jugador_actual['def'] < 0:
        jugador_actual['def'] = 0

def perdida_stats_por_shield(jugador_actual: dict, carta_jugador: dict):
    bonus = carta_jugador.get('bonus')
    jugador_actual['hp'] -= carta_jugador.get('atk') * bonus
    jugador_actual['atk'] -= carta_jugador.get('atk') * bonus
    jugador_actual['def'] -= carta_jugador.get('def') * bonus

    if jugador_actual['hp'] < 0:
        jugador_actual['hp'] = 0
    if jugador_actual['atk'] < 0:
        jugador_actual['atk'] = 0
    if jugador_actual['def'] < 0:
        jugador_actual['def'] = 0

def sumar_puntaje_actual(jugador_actual: dict, nuevo_puntaje: int):
    jugador_actual['puntaje_actual'] += nuevo_puntaje

def sumar_puntaje_carta_actual(jugador_actual: dict, carta_actual: int):
    jugador_actual['puntaje_actual'] += carta.get_puntaje_carta(carta_actual)

def get_puntaje_actual(jugador_actual: dict):
    return jugador_actual.get('puntaje_actual')

def get_puntaje_total(jugador_actual: dict):
    return jugador_actual.get('puntaje_total')

def get_nombre(jugador_actual: dict):
    return jugador_actual.get('nombre')

def actualizar_puntaje_total(jugador_actual: dict):
    jugador_actual['puntaje_total'] += jugador_actual.get('puntaje_actual')

def set_puntaje_actual(jugador_actual: dict, nuevo_puntaje: int):
    jugador_actual['puntaje_actual'] = nuevo_puntaje

def set_puntaje_total(jugador_actual: dict, nuevo_puntaje: int):
    jugador_actual['puntaje_total'] = nuevo_puntaje

def set_nombre(jugador_actual: dict, nuevo_puntaje: int):
    jugador_actual['nombre'] = nuevo_puntaje
