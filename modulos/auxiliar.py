import pygame as pg
import modulos.variables as var
import json
import os


def mostrar_texto(surface: pg.Surface, texto: str, pos: tuple, font, color = pg.Color('black')):
    words = []

    for word in texto.splitlines():
        words.append(word.split(' '))

    space = font.size(' ')[0]
    ancho_max, alto_max = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, False, color)
            ancho_palabra, alto_palabra = word_surface.get_size()
            if x + ancho_palabra >= ancho_max:
                x = pos[0]
                y += alto_palabra
            surface.blit(word_surface, (x, y))
            x += ancho_palabra + space
        x = pos[0]
        y += alto_palabra

def crear_cuadro(dimensiones: tuple, coordenadas: tuple, color: tuple) -> dict:
    cuadro = {}
    cuadro['superficie'] = pg.Surface(dimensiones)
    cuadro['rectangulo'] = cuadro.get('superficie').get_rect()
    cuadro['rectangulo'].topleft = coordenadas
    cuadro['superficie'].fill(pg.Color(color))
    return cuadro

def parsear_entero(valor: str):
    """
    Convierte un string a entero con manejo de errores

    Args:
        valor: String a convertir

    Returns:
        int o None si la conversión falla
    """
    try:
        return int(valor.strip())
    except (ValueError, AttributeError):

        return None

def mapear_valores(matriz: list[list], indice_a_aplicar: int, callback):
    """
    Aplica una función callback a una columna específica de una matriz

    Args:
        matriz: Matriz de listas a procesar
        indice_a_aplicar: Índice de la columna a transformar
        callback: Función a aplicar a cada valor de la columna
    """
    for indice_fila in range(len(matriz)):
        valor = matriz[indice_fila][indice_a_aplicar]
        matriz[indice_fila][indice_a_aplicar] = callback(valor)

def cargar_ranking():
    """
    Carga el ranking desde el archivo CSV con validación de datos

    Returns:
        list: Lista de [nombre, puntos] ordenada por puntos descendente
    """
    ranking = []

    try:
        with open(var.RUTA_RANKING_CSV, 'r', encoding='utf-8') as file:
            lineas = file.readlines()


            for numero_linea, linea in enumerate(lineas, 1):
                linea = linea.strip()
                if linea:
                    partes = linea.split(',')


                    if len(partes) == 2:
                        nombre = partes[0].strip()
                        puntos_str = partes[1].strip()


                        if nombre:
                            puntos = parsear_entero(puntos_str)


                            if puntos is not None and puntos >= 0:
                                ranking.append([nombre, puntos])


        ranking.sort(key=lambda fila: fila[1], reverse=True)

        return ranking

    except FileNotFoundError:

        ranking_default = [
            ["Goku", 1500],
            ["Vegeta", 1400],
            ["Gohan", 1200],
            ["Piccolo", 1100],
            ["Trunks", 900],
            ["Krillin", 800],
            ["Yamcha", 500]
        ]
        guardar_ranking(ranking_default)
        return ranking_default

    except Exception as e:

        return []

def guardar_ranking(ranking_completo: list):
    """
    Guarda el ranking completo en el archivo CSV

    Args:
        ranking_completo: Lista de [nombre, puntos] a guardar
    """
    try:
        with open(var.RUTA_RANKING_CSV, 'w', encoding='utf-8') as file:
            for jugador in ranking_completo:
                if len(jugador) >= 2:
                    nombre = str(jugador[0]).strip()
                    puntos = int(jugador[1])


                    if nombre and puntos >= 0:
                        data = f'{nombre},{puntos}\n'
                        file.write(data)

    except Exception as e:

        pass


def cargar_configs(path: str) -> dict:
    """
    Carga configuraciones desde un archivo JSON

    Args:
        path: Ruta al archivo de configuración

    Returns:
        dict: Diccionario con las configuraciones cargadas
    """
    configuraciones = {}
    with open(path, 'r', encoding='utf-8') as file:
        configuraciones = json.load(file)
    return configuraciones

def achicar_imagen_card(path_imagen: str, porcentaje: int):
    imagen_raw = pg.image.load(path_imagen)
    alto = int(imagen_raw.get_height() * float(f'0.{porcentaje}'))
    ancho = int(imagen_raw.get_width() * float(f'0.{porcentaje}'))
    imagen_final = pg.transform.scale(imagen_raw, (ancho, alto))
    return imagen_final

def generar_bd(root_path_cards: str):
    carta_dict = {
        "cartas": {}
    }

    for root, dir, files in os.walk(root_path_cards, topdown=True):
        reverse_path = ''
        deck_cards = []
        deck_name = root.split('\\')[-1]

        for file in files:
            path_card = os.path.join(root, file)

            if 'reverse' in path_card:
                reverse_path = path_card
            else:
                file = file.replace('\\', '/')
                filename = os.path.splitext(file)[0]
                datos = filename.split('_')

                id = datos[0]
                hp = int(datos[2])
                atk = int(datos[4])
                deff = int(datos[6])
                bonus = int(datos[7])

                card = {
                    'id': id,
                    "nombre": '',
                    "hp": hp,
                    "atk": atk,
                    "def": deff,
                    "bonus": bonus,
                    'puntaje': '',
                    "path_imagen_frente": path_card
                }
                deck_cards.append(card)

        for index_card in range(len(deck_cards)):
            deck_cards[index_card]['path_imagen_reverso'] = reverse_path

        carta_dict['cartas'][deck_name] = deck_cards
    return carta_dict

def guardar_bd(diccionario: dict, path: str):
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(diccionario, file, indent=4)

bd = generar_bd('./assets_Dragon_Ball_Trading_Card_Game/img/decks')
guardar_bd(bd, 'mazo.json')
