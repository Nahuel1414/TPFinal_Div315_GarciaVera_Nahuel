from modulos.jugador import calcular_stats_mazo
import random as rd
import modulos.carta as carta

def asignar_mazo_enemy(nivel_data: dict):
    """
    Asigna un mazo aleatorio al enemy, diferente al del jugador
    """

    if 'mazos_disponibles' not in nivel_data or 'mazo_jugador_seleccionado' not in nivel_data:
        return

    mazos_disponibles = nivel_data['mazos_disponibles']
    mazo_jugador_seleccionado = nivel_data['mazo_jugador_seleccionado']


    mazos_enemy = [mazo for mazo in mazos_disponibles if mazo != mazo_jugador_seleccionado]

    if not mazos_enemy:
        return


    mazo_enemy = rd.choice(mazos_enemy)


    nivel_data['mazo_enemy_seleccionado'] = mazo_enemy

    cartas_mazo = nivel_data['cartas_mazo_juego'][mazo_enemy]

    coords_mazo = nivel_data['configs']['coordenadas']['mazo_enemy']
    coords_jugada = nivel_data['configs']['coordenadas']['jugada_enemy']

    nivel_data['cartas_mazo_enemy'] = []


    for carta_data in cartas_mazo:
        carta_mazo = carta.inicializar_carta(carta_data, coords_mazo)
        carta_mazo['visible'] = False
        nivel_data['cartas_mazo_enemy'].append(carta_mazo)

def inicializar_enemy(mazo= None):
    enemy_actual = {}

    enemy_actual['puntaje_actual'] = 0
    enemy_actual['puntaje_total'] = 0
    enemy_actual['nombre'] = 'enemy'
    enemy_actual['heal_usado'] = False
    enemy_actual['shield_usado'] = False
    enemy_actual['shield_activo'] = False

    if mazo:
        hp, atk, df = calcular_stats_mazo(mazo)
        enemy_actual['hp'] = hp
        enemy_actual['atk'] = atk
        enemy_actual['def'] = df
        enemy_actual['hp_inicial'] = hp
    else:
        enemy_actual['hp'] = 100
        enemy_actual['atk'] = 10
        enemy_actual['def'] = 10
        enemy_actual['hp_inicial'] = 100

    return enemy_actual

def perdida_stats_enemy(enemy_actual: dict, carta_enemy: dict):
    bonus = carta_enemy.get('bonus')
    enemy_actual['hp'] -= carta_enemy.get('atk', 0) * bonus
    enemy_actual['atk'] -= carta_enemy.get('atk', 0) * bonus
    enemy_actual['def'] -= carta_enemy.get('def', 0) * bonus
    if enemy_actual['hp'] < 0:
        enemy_actual['hp'] = 0
    if enemy_actual['atk'] < 0:
        enemy_actual['atk'] = 0
    if enemy_actual['def'] < 0:
        enemy_actual['def'] = 0

def usar_heal(enemy_actual: dict):
    if not enemy_actual.get('heal_usado', False):
        enemy_actual['hp'] = enemy_actual.get('hp_inicial', enemy_actual['hp'])
        enemy_actual['heal_usado'] = True
