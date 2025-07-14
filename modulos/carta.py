import pygame as pg
import modulos.auxiliar as aux

def inicializar_carta(carta_dict: dict, coordenadas: tuple[int,int]) -> dict:
    carta_dict_final = {}
    carta_dict_final['id'] = carta_dict.get('id')
    carta_dict_final['nombre'] = carta_dict.get('nombre')
    carta_dict_final['hp'] = carta_dict.get('hp')
    carta_dict_final['atk'] = carta_dict.get('atk')
    carta_dict_final['def'] = carta_dict.get('def')
    carta_dict_final['estrellas'] = carta_dict.get('bonus')
    carta_dict_final['puntaje'] = carta_dict.get('puntaje')
    carta_dict_final['path_imagen_frente'] = carta_dict.get('path_imagen_frente')
    carta_dict_final['path_imagen_reverso'] = carta_dict.get('path_imagen_reverso')

    carta_dict_final['visible'] = False
    carta_dict_final['imagen'] = aux.achicar_imagen_card(carta_dict_final.get('path_imagen_frente'), 45)
    carta_dict_final['imagen_reverso'] = aux.achicar_imagen_card(carta_dict_final.get('path_imagen_reverso'), 45)

    carta_dict_final['rect'] = carta_dict_final.get('imagen').get_rect()
    carta_dict_final['rect'].x = coordenadas['x']
    carta_dict_final['rect'].y = coordenadas['y']

    carta_dict_final['rect_reverso'] = carta_dict_final.get('imagen_reverso').get_rect()
    carta_dict_final['rect_reverso'].x = coordenadas['x']
    carta_dict_final['rect_reverso'].y = coordenadas['y']

    return carta_dict_final

def get_puntaje_carta(card_dict: dict):

    puntaje_carta = card_dict.get('puntaje')
    if puntaje_carta and str(puntaje_carta).isdigit():
        return int(puntaje_carta)



    atk = card_dict.get('atk', 0)
    return max(1, int(atk / 10))

def set_puntaje(card_dict: dict, puntaje: int):
    card_dict['puntaje'] = puntaje

def draw_carta(card_data: dict, screen: pg.Surface):

    if card_data.get('visible'):
        screen.blit(card_data.get('imagen'), card_data.get('rect'))
    else:
        screen.blit(card_data.get('imagen_reverso'), card_data.get('rect_reverso'))

def asignar_coordenadas_carta(carta_dict: dict, nueva_coordenada: tuple[int,int]):
    """
    Asigna nuevas coordenadas a una carta

    Args:
        carta_dict: Diccionario con los datos de la carta
        nueva_coordenada: Tupla con las nuevas coordenadas (x, y)
    """
    if nueva_coordenada is None:
        return

    if not isinstance(nueva_coordenada, (tuple, list)) or len(nueva_coordenada) != 2:
        return

    try:
        carta_dict['rect'].topleft = nueva_coordenada
        carta_dict['rect_reverso'].topleft = nueva_coordenada
    except Exception as e:
        pass

def cambiar_visibilidad_carta(carta_dict: dict):
    """
    Cambia la visibilidad de una carta a visible
    """
    carta_dict['visible'] = True

def iniciar_animacion_choque(carta_ganadora: dict, carta_perdedora: dict):
    """
    Inicia la animación de choque de la carta ganadora hacia la perdedora

    Args:
        carta_ganadora: Diccionario de la carta que ganó
        carta_perdedora: Diccionario de la carta que perdió
    """

    import pygame as pg
    try:
        sonido_hit = pg.mixer.Sound('./assets_Dragon_Ball_Trading_Card_Game/audio/sounds/hit_01.ogg')
        sonido_hit.play()
    except Exception as e:
        pass


    carta_ganadora['pos_original'] = (carta_ganadora['rect'].x, carta_ganadora['rect'].y)


    carta_ganadora['pos_objetivo'] = (carta_perdedora['rect'].x, carta_perdedora['rect'].y)


    carta_ganadora['animando'] = True
    carta_ganadora['tiempo_animacion'] = 0
    carta_ganadora['duracion_animacion'] = 1000

def actualizar_animacion_choque(carta_ganadora: dict, delta_time: int):
    """
    Actualiza la animación de choque frame por frame

    Args:
        carta_ganadora: Carta que está siendo animada
        delta_time: Tiempo transcurrido desde el último frame

    Returns:
        bool: True si la animación continúa, False si terminó
    """
    if not carta_ganadora.get('animando', False):
        return False

    carta_ganadora['tiempo_animacion'] += delta_time
    progreso = carta_ganadora['tiempo_animacion'] / carta_ganadora['duracion_animacion']

    if progreso >= 1.0:

        carta_ganadora['rect'].x = carta_ganadora['pos_original'][0]
        carta_ganadora['rect'].y = carta_ganadora['pos_original'][1]
        carta_ganadora['rect_reverso'].x = carta_ganadora['pos_original'][0]
        carta_ganadora['rect_reverso'].y = carta_ganadora['pos_original'][1]
        carta_ganadora['animando'] = False
        return False



    progreso_suavizado = 1 - (1 - progreso) ** 3

    pos_inicial = carta_ganadora['pos_original']
    pos_objetivo = carta_ganadora['pos_objetivo']


    nueva_x = pos_inicial[0] + (pos_objetivo[0] - pos_inicial[0]) * progreso_suavizado
    nueva_y = pos_inicial[1] + (pos_objetivo[1] - pos_inicial[1]) * progreso_suavizado


    carta_ganadora['rect'].x = int(nueva_x)
    carta_ganadora['rect'].y = int(nueva_y)
    carta_ganadora['rect_reverso'].x = int(nueva_x)
    carta_ganadora['rect_reverso'].y = int(nueva_y)

    return True

def resetear_animacion_carta(carta_dict: dict):
    """
    Resetea el estado de animación de una carta a su posición original

    Args:
        carta_dict: Diccionario de la carta a resetear
    """
    if carta_dict.get('pos_original'):
        carta_dict['rect'].x = carta_dict['pos_original'][0]
        carta_dict['rect'].y = carta_dict['pos_original'][1]
        carta_dict['rect_reverso'].x = carta_dict['pos_original'][0]
        carta_dict['rect_reverso'].y = carta_dict['pos_original'][1]


    carta_dict['animando'] = False
    carta_dict['tiempo_animacion'] = 0
    carta_dict['animando_volando'] = False
    carta_dict['tiempo_animacion_volando'] = 0
    carta_dict['rotacion_volando'] = 0
    carta_dict['animando_entrada'] = False
    carta_dict['tiempo_animacion_entrada'] = 0

def iniciar_animacion_salir_volando(carta_perdedora: dict):
    """
    Inicia la animación de "salir volando" para la carta perdedora

    Args:
        carta_perdedora: Diccionario de la carta que perdió
    """

    import pygame as pg
    try:
        sonido_critical = pg.mixer.Sound('./assets_Dragon_Ball_Trading_Card_Game/audio/sounds/critical_hit.ogg')
        sonido_critical.play()
    except Exception as e:
        pass


    carta_perdedora['pos_original'] = (carta_perdedora['rect'].x, carta_perdedora['rect'].y)


    import modulos.variables as var
    carta_perdedora['pos_objetivo'] = (
        carta_perdedora['rect'].x + 200,
        carta_perdedora['rect'].y - 300
    )


    carta_perdedora['animando_volando'] = True
    carta_perdedora['tiempo_animacion_volando'] = 0
    carta_perdedora['duracion_animacion_volando'] = 800
    carta_perdedora['rotacion_volando'] = 0

def actualizar_animacion_salir_volando(carta_perdedora: dict, delta_time: int):
    """
    Actualiza la animación de "salir volando" frame por frame

    Args:
        carta_perdedora: Carta que está siendo animada
        delta_time: Tiempo transcurrido desde el último frame

    Returns:
        bool: True si la animación continúa, False si terminó
    """
    if not carta_perdedora.get('animando_volando', False):
        return False

    carta_perdedora['tiempo_animacion_volando'] += delta_time
    progreso = carta_perdedora['tiempo_animacion_volando'] / carta_perdedora['duracion_animacion_volando']

    if progreso >= 1.0:

        carta_perdedora['visible'] = False
        carta_perdedora['animando_volando'] = False
        carta_perdedora['rotacion_volando'] = 0
        return False


    progreso_suavizado = 1 - (1 - progreso) ** 2

    pos_inicial = carta_perdedora['pos_original']
    pos_objetivo = carta_perdedora['pos_objetivo']


    nueva_x = pos_inicial[0] + (pos_objetivo[0] - pos_inicial[0]) * progreso_suavizado
    nueva_y = pos_inicial[1] + (pos_objetivo[1] - pos_inicial[1]) * progreso_suavizado


    carta_perdedora['rotacion_volando'] = progreso * 360


    carta_perdedora['rect'].x = int(nueva_x)
    carta_perdedora['rect'].y = int(nueva_y)
    carta_perdedora['rect_reverso'].x = int(nueva_x)
    carta_perdedora['rect_reverso'].y = int(nueva_y)

    return True

def iniciar_animacion_entrada(carta_dict: dict, pos_inicial: tuple, pos_final: tuple):
    """
    Inicia la animación de entrada cuando una carta se hace visible en la mesa

    Args:
        carta_dict: Diccionario de la carta
        pos_inicial: Posición inicial (desde el mazo)
        pos_final: Posición final (en la mesa)
    """

    import pygame as pg
    try:
        sonido_carta = pg.mixer.Sound('./assets_Dragon_Ball_Trading_Card_Game/audio/sounds/item.mp3')
        sonido_carta.set_volume(0.3)
        sonido_carta.play()
    except Exception as e:
        pass


    carta_dict['pos_inicial_entrada'] = pos_inicial
    carta_dict['pos_final_entrada'] = pos_final
    carta_dict['animando_entrada'] = True
    carta_dict['tiempo_animacion_entrada'] = 0
    carta_dict['duracion_animacion_entrada'] = 600


    carta_dict['rect'].x = pos_inicial[0]
    carta_dict['rect'].y = pos_inicial[1]
    carta_dict['rect_reverso'].x = pos_inicial[0]
    carta_dict['rect_reverso'].y = pos_inicial[1]

def actualizar_animacion_entrada(carta_dict: dict, delta_time: int):
    """
    Actualiza la animación de entrada frame por frame

    Args:
        carta_dict: Carta que está siendo animada
        delta_time: Tiempo transcurrido desde el último frame

    Returns:
        bool: True si la animación continúa, False si terminó
    """
    if not carta_dict.get('animando_entrada', False):
        return False

    carta_dict['tiempo_animacion_entrada'] += delta_time
    progreso = carta_dict['tiempo_animacion_entrada'] / carta_dict['duracion_animacion_entrada']

    if progreso >= 1.0:

        pos_final = carta_dict['pos_final_entrada']
        carta_dict['rect'].x = pos_final[0]
        carta_dict['rect'].y = pos_final[1]
        carta_dict['rect_reverso'].x = pos_final[0]
        carta_dict['rect_reverso'].y = pos_final[1]
        carta_dict['animando_entrada'] = False
        return False


    progreso_suavizado = 1 - (1 - progreso) ** 3

    pos_inicial = carta_dict['pos_inicial_entrada']
    pos_final = carta_dict['pos_final_entrada']


    nueva_x = pos_inicial[0] + (pos_final[0] - pos_inicial[0]) * progreso_suavizado
    nueva_y = pos_inicial[1] + (pos_final[1] - pos_inicial[1]) * progreso_suavizado


    carta_dict['rect'].x = int(nueva_x)
    carta_dict['rect'].y = int(nueva_y)
    carta_dict['rect_reverso'].x = int(nueva_x)
    carta_dict['rect_reverso'].y = int(nueva_y)

    return True
