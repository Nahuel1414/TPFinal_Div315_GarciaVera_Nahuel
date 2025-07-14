import pygame as pg
import modulos.jugador as jugador_mod
import modulos.enemy as enemy_mod
import modulos.forms.form_start_level as form_start_level
import modulos.nivel_cartas


def calcular_atk_con_bonus(atk: int, estrellas: int) -> float:
    """
    Calcula el ataque con bonus basado en las estrellas de la carta

    Args:
        atk: Valor base de ataque de la carta
        estrellas: Número de estrellas de la carta (1-7)

    Returns:
        float: Ataque con bonus aplicado
    """
    if estrellas == 1:
        bonus_porcentaje = 0.01
    elif estrellas == 2:
        bonus_porcentaje = 0.02
    elif estrellas == 3:
        bonus_porcentaje = 0.03
    elif estrellas == 4:
        bonus_porcentaje = 0.04
    elif estrellas == 5:
        bonus_porcentaje = 0.05
    elif estrellas == 6:
        bonus_porcentaje = 0.06
    elif estrellas == 7:
        bonus_porcentaje = 0.07
    elif estrellas == 8:
        bonus_porcentaje = 0.10
    else:
        bonus_porcentaje = 0.0

    return atk * (1 + bonus_porcentaje)


def calcular_stats_con_bonus(carta: dict) -> dict:
    """
    Calcula todos los stats de una carta con bonus basado en las estrellas

    Args:
        carta: Diccionario con los datos de la carta

    Returns:
        dict: Stats calculados con bonus aplicado
    """
    estrellas = carta['estrellas']

    if estrellas == 1:
        bonus_porcentaje = 0.01
    elif estrellas == 2:
        bonus_porcentaje = 0.02
    elif estrellas == 3:
        bonus_porcentaje = 0.03
    elif estrellas == 4:
        bonus_porcentaje = 0.04
    elif estrellas == 5:
        bonus_porcentaje = 0.05
    elif estrellas == 6:
        bonus_porcentaje = 0.06
    elif estrellas == 7:
        bonus_porcentaje = 0.07
    elif estrellas == 8:
        bonus_porcentaje = 0.10
    else:
        bonus_porcentaje = 0.0

    return {
        'hp': int(carta['hp'] * (1 + bonus_porcentaje)),
        'atk': int(carta['atk'] * (1 + bonus_porcentaje)),
        'def': int(carta['def'] * (1 + bonus_porcentaje))
    }


def partida(nivel_data: dict):
    """
    Función principal que ejecuta una mano de batalla entre jugador y enemy

    Args:
        nivel_data: Diccionario con todos los datos del nivel actual

    Returns:
        dict: Resultado de la batalla con ganador, puntos y estado de terminación
    """
    jugador = nivel_data["jugador"]
    enemy = nivel_data["enemy"]


    cartas_jugador = nivel_data.get('cartas_mazo_jugador_vistas')
    cartas_enemy = nivel_data.get('cartas_mazo_enemy_vistas')


    if not cartas_jugador or not cartas_enemy:
        return {"ganador": None}


    if enemy is None:
        return {"ganador": None}


    carta_jugador = cartas_jugador[-1]
    carta_enemy = cartas_enemy[-1]


    atk_jugador = calcular_atk_con_bonus(carta_jugador['atk'], carta_jugador['estrellas'])
    atk_enemy = calcular_atk_con_bonus(carta_enemy['atk'], carta_enemy['estrellas'])

    resultado = {"ganador": None}
    puntos_ganados = 0


    if atk_jugador > atk_enemy:
        resultado['ganador'] = 'jugador'


        if enemy['shield_activo']:
            enemy['shield_activo'] = False
            reproducir_sonido_shield_desactivado()

            stats_carta_jugador = calcular_stats_con_bonus(carta_jugador)
            jugador['hp'] -= stats_carta_jugador['hp']
            jugador['atk'] -= stats_carta_jugador['atk']
            jugador['def'] -= stats_carta_jugador['def']
        else:

            stats_carta_enemy = calcular_stats_con_bonus(carta_enemy)
            enemy['hp'] -= stats_carta_enemy['hp']
            enemy['atk'] -= stats_carta_enemy['atk']
            enemy['def'] -= stats_carta_enemy['def']


        tiempo_restante = nivel_data.get('level_timer', 0)

        puntos_ganados = calcular_puntos_mano(carta_jugador, carta_enemy, tiempo_restante, False)
        jugador['puntaje_actual'] += puntos_ganados

    elif atk_enemy > atk_jugador:
        resultado['ganador'] = 'enemy'


        if jugador['shield_activo']:
            jugador['shield_activo'] = False
            reproducir_sonido_shield_desactivado()

            stats_carta_enemy = calcular_stats_con_bonus(carta_enemy)
            enemy['hp'] -= stats_carta_enemy['hp']
            enemy['atk'] -= stats_carta_enemy['atk']
            enemy['def'] -= stats_carta_enemy['def']


            tiempo_restante = nivel_data.get('level_timer', 0)

            puntos_ganados = calcular_puntos_mano(carta_enemy, carta_jugador, tiempo_restante, True)
            jugador['puntaje_actual'] += puntos_ganados
        else:

            stats_carta_enemy = calcular_stats_con_bonus(carta_enemy)
            jugador['hp'] -= stats_carta_enemy['hp']
            jugador['atk'] -= stats_carta_enemy['atk']
            jugador['def'] -= stats_carta_enemy['def']
    else:

        resultado['ganador'] = 'empate'


    resultado['puntos_ganados'] = puntos_ganados
    resultado['puntaje_total'] = jugador['puntaje_actual']


    if jugador['hp'] < 0:
        jugador['hp'] = 0
    if jugador['atk'] < 0:
        jugador['atk'] = 0
    if jugador['def'] < 0:
        jugador['def'] = 0

    if enemy['hp'] < 0:
        enemy['hp'] = 0

    if enemy['hp'] < 0:
        enemy['hp'] = 0
    if enemy['atk'] < 0:
        enemy['atk'] = 0
    if enemy['def'] < 0:
        enemy['def'] = 0


    if jugador['hp'] <= 0:
        resultado['ganador'] = 'enemy'
        resultado['batalla_terminada'] = {
            'terminada': True,
            'ganador': 'enemy',
            'razon': 'hp_jugador_0',
            'mensaje': 'El jugador se quedó sin vida'
        }
        return resultado

    if enemy['hp'] <= 0:
        resultado['ganador'] = 'jugador'
        resultado['batalla_terminada'] = {
            'terminada': True,
            'ganador': 'jugador',
            'razon': 'hp_enemy_0',
            'mensaje': 'El enemy se quedó sin vida'
        }
        return resultado


    batalla_terminada = verificar_fin_batalla(nivel_data)
    resultado['batalla_terminada'] = batalla_terminada


    if batalla_terminada.get('terminada'):
        resultado['ganador'] = batalla_terminada.get('ganador')

    return resultado


def verificar_fin_batalla(nivel_data: dict) -> dict:
    """
    Verifica si la batalla ha terminado por cartas agotadas

    El ganador será quien tenga más HP cuando se acaben las cartas según el
    requisito académico: "Cuando se llega al final de las cartas, el ganador
    será quien mas HP tenga"

    Nota: La verificación de HP = 0 se hace inmediatamente en partida()

    Args:
        nivel_data: Diccionario con los datos del nivel actual

    Returns:
        dict: Estado de terminación con ganador y mensaje
    """

    cartas_jugador = nivel_data.get('cartas_mazo_jugador', [])
    cartas_enemy = nivel_data.get('cartas_mazo_enemy', [])


    cartas_jugador_restantes = [carta for carta in cartas_jugador if not carta.get('visible', False)]
    cartas_enemy_restantes = [carta for carta in cartas_enemy if not carta.get('visible', False)]


    if len(cartas_jugador_restantes) <= 0 or len(cartas_enemy_restantes) <= 0:

        jugador = nivel_data.get('jugador', {})
        enemy = nivel_data.get('enemy', {})

        hp_jugador = jugador.get('hp', 0)
        hp_enemy = enemy.get('hp', 0)

        if hp_jugador > hp_enemy:
            return {
                'terminada': True,
                'ganador': 'jugador',
                'razon': 'cartas_agotadas_hp_mayor',
                'mensaje': f'Cartas agotadas: Jugador gana con {hp_jugador} HP vs {hp_enemy} HP'
            }
        elif hp_enemy > hp_jugador:
            return {
                'terminada': True,
                'ganador': 'enemy',
                'razon': 'cartas_agotadas_hp_mayor',
                'mensaje': f'Cartas agotadas: Enemy gana con {hp_enemy} HP vs {hp_jugador} HP'
            }
        else:
            return {
                'terminada': True,
                'ganador': 'empate',
                'razon': 'cartas_agotadas_empate',
                'mensaje': f'Cartas agotadas: Empate con {hp_jugador} HP cada uno'
            }


    return {
        'terminada': False,
        'ganador': None,
        'razon': None,
        'mensaje': None
    }


def puede_continuar_batalla(nivel_data: dict) -> bool:
    """
    Función auxiliar que retorna True si la batalla puede continuar,
    False si ha terminado por alguna condición de fin
    """
    resultado_verificacion = verificar_fin_batalla(nivel_data)
    return not resultado_verificacion['terminada']


def obtener_ganador_batalla(nivel_data: dict) -> dict:
    """
    Función auxiliar que retorna información del ganador si la batalla terminó
    """
    return verificar_fin_batalla(nivel_data)


def usar_comodin_heal(jugador: dict) -> bool:
    """
    Usa el comodín HEAL para recuperar toda la vida perdida
    Retorna True si se pudo usar, False si ya fue usado
    """
    if jugador.get('heal_usado', False):
        return False

    if 'hp_inicial' in jugador:
        jugador['hp'] = jugador['hp_inicial']
        jugador['heal_usado'] = True
        return True
    return False

def usar_comodin_shield(jugador: dict) -> bool:
    """
    Usa el comodín SHIELD para protegerse en la siguiente jugada
    Retorna True si se pudo usar, False si ya fue usado
    """
    if jugador.get('shield_usado', False):
        return False

    jugador['shield_activo'] = True
    jugador['shield_usado'] = True
    return True

def calcular_puntos_mano(carta_ganadora: dict, carta_perdedora: dict, tiempo_restante: int = 0, uso_shield: bool = False) -> int:
    """
    Calcula los puntos ganados en una mano según diferentes factores:
    - Puntaje base: ATK ganadora - DEF perdedora
    - Bonus por tiempo: +1 punto por cada 10 segundos restantes
    - Bonus por shield: +50 puntos extra si se usó shield exitosamente
    """

    stats_ganadora = calcular_stats_con_bonus(carta_ganadora)
    stats_perdedora = calcular_stats_con_bonus(carta_perdedora)


    puntaje_base = max(10, stats_ganadora['atk'] - stats_perdedora['def'])


    bonus_tiempo = max(0, tiempo_restante // 10)


    bonus_shield = 50 if uso_shield else 0

    puntaje_total = puntaje_base + bonus_tiempo + bonus_shield

    return puntaje_total

def calcular_resultado_batalla(nivel_data: dict):
    """
    Calcula el resultado de una batalla sin aplicar los cambios a las stats

    Args:
        nivel_data: Diccionario con todos los datos del nivel actual

    Returns:
        dict: Resultado de la batalla con ganador, cambios a aplicar y estado de terminación
    """
    jugador = nivel_data["jugador"]
    enemy = nivel_data["enemy"]


    cartas_jugador = nivel_data.get('cartas_mazo_jugador_vistas')
    cartas_enemy = nivel_data.get('cartas_mazo_enemy_vistas')


    if not cartas_jugador or not cartas_enemy:
        return {"ganador": None}


    if enemy is None:
        return {"ganador": None}


    carta_jugador = cartas_jugador[-1]
    carta_enemy = cartas_enemy[-1]


    atk_jugador = calcular_atk_con_bonus(carta_jugador['atk'], carta_jugador['estrellas'])
    atk_enemy = calcular_atk_con_bonus(carta_enemy['atk'], carta_enemy['estrellas'])

    resultado = {"ganador": None}
    puntos_ganados = 0


    if atk_jugador > atk_enemy:
        resultado['ganador'] = 'jugador'


        if enemy['shield_activo']:

            stats_carta_jugador = calcular_stats_con_bonus(carta_jugador)
            resultado['cambios'] = {
                'jugador': {
                    'hp': -stats_carta_jugador['hp'],
                    'atk': -stats_carta_jugador['atk'],
                    'def': -stats_carta_jugador['def']
                },
                'enemy': {'shield_activo': False}
            }
        else:

            stats_carta_enemy = calcular_stats_con_bonus(carta_enemy)
            resultado['cambios'] = {
                'enemy': {
                    'hp': -stats_carta_enemy['hp'],
                    'atk': -stats_carta_enemy['atk'],
                    'def': -stats_carta_enemy['def']
                }
            }


        tiempo_restante = nivel_data.get('level_timer', 0)
        puntos_ganados = calcular_puntos_mano(carta_jugador, carta_enemy, tiempo_restante, False)
        resultado['cambios']['jugador'] = resultado['cambios'].get('jugador', {})
        resultado['cambios']['jugador']['puntaje_actual'] = puntos_ganados

    elif atk_enemy > atk_jugador:
        resultado['ganador'] = 'enemy'

        if jugador['shield_activo']:

            stats_carta_enemy = calcular_stats_con_bonus(carta_enemy)
            resultado['cambios'] = {
                'enemy': {
                    'hp': -stats_carta_enemy['hp'],
                    'atk': -stats_carta_enemy['atk'],
                    'def': -stats_carta_enemy['def']
                },
                'jugador': {'shield_activo': False}
            }


            tiempo_restante = nivel_data.get('level_timer', 0)
            puntos_ganados = calcular_puntos_mano(carta_enemy, carta_jugador, tiempo_restante, True)
            resultado['cambios']['jugador']['puntaje_actual'] = puntos_ganados
        else:

            stats_carta_enemy = calcular_stats_con_bonus(carta_enemy)
            resultado['cambios'] = {
                'jugador': {
                    'hp': -stats_carta_enemy['hp'],
                    'atk': -stats_carta_enemy['atk'],
                    'def': -stats_carta_enemy['def']
                }
            }
    else:

        resultado['ganador'] = 'empate'
        resultado['cambios'] = {}


    resultado['puntos_ganados'] = puntos_ganados


    jugador_hp_final = jugador['hp']
    enemy_hp_final = enemy['hp']


    if 'cambios' in resultado:
        if 'jugador' in resultado['cambios'] and 'hp' in resultado['cambios']['jugador']:
            jugador_hp_final += resultado['cambios']['jugador']['hp']
        if 'enemy' in resultado['cambios'] and 'hp' in resultado['cambios']['enemy']:
            enemy_hp_final += resultado['cambios']['enemy']['hp']


    if jugador_hp_final < 0:
        jugador_hp_final = 0
    if enemy_hp_final < 0:
        enemy_hp_final = 0


    if jugador_hp_final <= 0:
        resultado['ganador'] = 'enemy'
        resultado['batalla_terminada'] = {
            'terminada': True,
            'ganador': 'enemy',
            'razon': 'hp_jugador_0',
            'mensaje': 'El jugador se quedó sin vida'
        }
        return resultado

    if enemy_hp_final <= 0:
        resultado['ganador'] = 'jugador'
        resultado['batalla_terminada'] = {
            'terminada': True,
            'ganador': 'jugador',
            'razon': 'hp_enemy_0',
            'mensaje': 'El enemy se quedó sin vida'
        }
        return resultado


    cartas_mazo_jugador = nivel_data.get('cartas_mazo_jugador', [])
    cartas_mazo_enemy = nivel_data.get('cartas_mazo_enemy', [])

    if len(cartas_mazo_jugador) == 0 or len(cartas_mazo_enemy) == 0:

        if jugador_hp_final > enemy_hp_final:
            ganador_final = 'jugador'
        elif enemy_hp_final > jugador_hp_final:
            ganador_final = 'enemy'
        else:
            ganador_final = 'empate'

        resultado['batalla_terminada'] = {
            'terminada': True,
            'ganador': ganador_final,
            'razon': 'cartas_agotadas',
            'mensaje': 'Se terminaron las cartas'
        }

    return resultado

def aplicar_cambios_batalla(nivel_data: dict, cambios: dict):
    """
    Aplica los cambios calculados por calcular_resultado_batalla

    Args:
        nivel_data: Diccionario con todos los datos del nivel actual
        cambios: Diccionario con los cambios a aplicar
    """
    jugador = nivel_data["jugador"]
    enemy = nivel_data["enemy"]


    if 'jugador' in cambios:
        cambios_jugador = cambios['jugador']
        if 'hp' in cambios_jugador:
            jugador['hp'] += cambios_jugador['hp']
        if 'atk' in cambios_jugador:
            jugador['atk'] += cambios_jugador['atk']
        if 'def' in cambios_jugador:
            jugador['def'] += cambios_jugador['def']
        if 'puntaje_actual' in cambios_jugador:
            jugador['puntaje_actual'] += cambios_jugador['puntaje_actual']
        if 'shield_activo' in cambios_jugador:

            if jugador['shield_activo'] and not cambios_jugador['shield_activo']:
                reproducir_sonido_shield_desactivado()
            jugador['shield_activo'] = cambios_jugador['shield_activo']


    if 'enemy' in cambios:
        cambios_enemy = cambios['enemy']
        if 'hp' in cambios_enemy:
            enemy['hp'] += cambios_enemy['hp']
        if 'atk' in cambios_enemy:
            enemy['atk'] += cambios_enemy['atk']
        if 'def' in cambios_enemy:
            enemy['def'] += cambios_enemy['def']
        if 'shield_activo' in cambios_enemy:

            if enemy['shield_activo'] and not cambios_enemy['shield_activo']:
                reproducir_sonido_shield_desactivado()
            enemy['shield_activo'] = cambios_enemy['shield_activo']


    if jugador['hp'] < 0:
        jugador['hp'] = 0
    if jugador['atk'] < 0:
        jugador['atk'] = 0
    if jugador['def'] < 0:
        jugador['def'] = 0

    if enemy['hp'] < 0:
        enemy['hp'] = 0
    if enemy['atk'] < 0:
        enemy['atk'] = 0
    if enemy['def'] < 0:
        enemy['def'] = 0

def reproducir_sonido_shield_desactivado():
    """
    Reproduce el sonido de shield desactivado
    """
    try:
        sonido_shield_deactivated = pg.mixer.Sound('./assets_Dragon_Ball_Trading_Card_Game/audio/sounds/shield_deactivated.ogg')
        sonido_shield_deactivated.play()
    except Exception as e:
        pass
