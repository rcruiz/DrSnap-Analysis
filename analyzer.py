import json
import os
import parser
import sys
from statistics import mean
from parser import ParserXML

PATH_JSON_SNAP_PROJECT = os.path.dirname(os.path.abspath(__file__)) + '/' + 'data.json'
PATH_JSON_BLOCKS_CATEGORIES = os.path.dirname(os.path.abspath(__file__)) + '/' + 'all.json'


def blocks_script(data):
    flag_anterior = 0
    resultado = False
    for element in data['sprites']:
        flag_actual = element['script']
        if flag_anterior == flag_actual:
            resultado = True
            break
        else:
            flag_anterior = element['script']
    return resultado

def number_script(data):
    try:
        n = data['sprites'][-1]['script']
        return n
    except IndexError:
        return 0

def number_sprite(data):
    try:
        n = data['sprites'][-1]['sprite']
        return n
    except IndexError:
        return 1

def puntuacion_paralelismo(data):
    puntuacion_bajo = 0
    puntuacion_medio = 0
    puntuacion_avanzado = 0
    basic = False
    med = False
    # calculamos los scripts y sprites
    n_script = number_script(data)
    n_sprite = number_sprite(data)
    # primera condicion tabla
    if n_sprite == 1 and n_script >= 2:
        basic = True
    elif n_sprite >= 2 and n_script >= 1:
        med = True
    # segunda condicion tabla
    for element in data['sprites']:
        if (element['block'] == 'receiveGo' or element['block'] == 'receiveKey') and basic:
            puntuacion_bajo = 1
        elif (element['block'] == 'receiveGo' or element['block'] == 'receiveKey') and med:
            puntuacion_medio = 2
        elif element['block'] == 'receiveCondition' or element['block'] == 'receiveMessage' or element['block'] == 'receiveOnClone':
            puntuacion_avanzado = 3
            break
        else:
            pass
    return max(puntuacion_bajo, puntuacion_medio, puntuacion_avanzado)

def puntuacion_condicionales(data):
    switch_condicionales = {
        'doIf': 1,
        'doIfElse': 2,
        'reportIfElse': 2,
        'reportAnd': 3,
        'reportOr': 3,
        'reportNot': 3
    }
    mayor = 0
    for element in data['sprites']:
        actual = switch_condicionales.get(element['block'])
        if actual is not None and mayor < actual:
            mayor = actual
            if mayor == 3:
                #mayor puntuacion no hace falta buscar mas
                break
    return mayor

def puntuacion_representacion_datos(data):
    switch_datos = {
        "forward": 1,
        "turn": 1,
        "turnLeft": 1,
        "setHeading": 1,
        "doFaceTowards": 1,
        "gotoXY": 1,
        "doGoToObject": 1,
        "doGlide": 1,
        "changeXPosition": 1,
        "setXPosition": 1,
        "changeYPosition": 1,
        "setYPosition": 1,
        "bounceOffEdge": 1,
        "doWearNextCostume": 1,
        "doSwitchToCostume": 1,
        "reportGetImageAttribute": 1,
        "reportNewCostumeStretched": 1,
        "reportNewCostume": 1,
        "changeEffect": 1,
        "changeScale": 1,
        "setScale": 1,
        "doSetVar": 2,
        "doChangeVar": 1,
        "doShowVar": 2,
        "doHideVar": 2,
        "doDeclareVariables": 2,
        "reportNewList": 3,
        "reportCONS": 3,
        "reportListItem": 3,
        "reportCDR": 3,
        "reportListLength": 3,
        "reportListIndex": 3,
        "reportListContainsItem": 3,
        "reportListIsEmpty": 3,
        "reportMap": 3,
        "reportKeep": 3,
        "reportFindFirst": 3,
        "reportCombine": 3,
        "reportConcatenatedLists": 3,
        "doAddToList": 3,
        "doDeleteFromList": 3,
        "doInsertInList": 3,
        "doReplaceInList": 3,
        "reportNumbers": 3}
    mayor = 0
    for element in data['sprites']:
        actual = switch_datos.get(element['block'])
        if actual != None and mayor < actual:
            mayor = actual
            if mayor == 3:
                break
    return mayor

def puntuacion_interactividad(data):
    switch_interactividad= {
        'receiveGo': 1,
        'receiveKey': 1,
        'receiveInteraction': 2,
        'reportKeyPressed': 2,
        'doAsk': 3,
        'reportTouchingObject': 2,
        'reportTouchingColor': 3,
        'reportColorIsTouchingColor': 3,
        'reportMouseDown': 3,
        'reportVideo': 3,
        'reportGlobalFlag': 3,
        'reportAudio': 3,
    }
    mayor= 0
    for element in data['sprites']:
        actual = switch_interactividad.get(element['block'])
        if actual!= None and mayor < actual :
            mayor = actual
            if mayor ==3:
                break
    return mayor

def puntuacion_sincronizacion(data):
    mayor = 0
    #creamos un switch que nos de la  puntuación correspondiente
    switch_sincronizacion = {
        'doWait':1,
        'doBroadcast':2,
        'receiveMessage':2,
        'doStopThis':2,
        'doPauseAll':2,
        'doWaitUntil':3,
        'doBroadcastAndWait':3,
        'receiveCondition':3,
        'receiveOnClone':3
    }
    for element in data['sprites']:
        actual = switch_sincronizacion.get(element['block'])
        if actual!= None and mayor < actual:
            mayor = actual
            if mayor ==3:
                break
    return mayor

def control_flujo(data):
    switch_flujo = {
        'doForever':2,
        'doRepeat':2,
        'doWaitUntil':3,
        'doUntil':3,
        'for':3
    }
    mayor = 0
    puntuacion_bajo =0
    resultado = blocks_script(data)
    if resultado:
        puntuacion_bajo = 1
    for element in data['sprites']:
        actual = switch_flujo.get(element['block'])
        if actual!= None and mayor < actual :
            mayor = actual
            if mayor==3:
                break
    return max(puntuacion_bajo, mayor)

def puntuacion_abstraccion(data):
    n_script = number_script(data)
    n_sprite = number_sprite(data)
    puntuacion_bajo = 0
    puntuacion_medio = 0
    puntuacion_avanzado = 0
    if  n_sprite == 1 and n_script >=2:
        puntuacion_bajo = 1
    elif n_sprite >= 2 and n_script >= 2:
        puntuacion_medio = 2
    if  data['block-definition']:
        puntuacion_avanzado = 3
    return max(puntuacion_bajo, puntuacion_medio, puntuacion_avanzado)

def categorias(data):
    dicc_categorias = {"motion": False, "looks": False, "sound": False,
                       "pen": False, "control": False, "sensing": False,
                       "operators": False, "variables": False}
    with open(PATH_JSON_BLOCKS_CATEGORIES) as file2:
        diccionario_all= json.load(file2)
    for element in data['sprites']:
        categoria = diccionario_all.get(element['block'])
        dicc_categorias[categoria] = True
    puntuacion = 0
    categorias = dicc_categorias.values()
    for categoria in categorias:
        if categoria == True:
            puntuacion = puntuacion + 1
    if puntuacion <=2:
         return 1
    elif puntuacion>2 and puntuacion <=6:
        return 2
    else:
        return 3

def switch_puntuacion(media):
    if media <0.5:
        return 0
    elif media <1.5:
        return 1
    elif media <2.5:
        return 2
    else:
        return 3

def calcular_puntuacion(file_xml):
    switch_nivel= {
        0:'No level',
        1:'Basic',
        2:'Intermediate',
        3:'Advanced'
    }
    ParserXML(file_xml)
    with open(PATH_JSON_SNAP_PROJECT) as file:
        data = json.load(file)
    name_project = (data['project_name'][0]['name']).strip(" \r\n")
    condicionales = puntuacion_condicionales(data)
    sincronizacion = puntuacion_sincronizacion(data)
    flujo = control_flujo(data)
    abstraccion = puntuacion_abstraccion(data)
    paralelismo = puntuacion_paralelismo(data)
    categoria = categorias(data)
    interactividad =puntuacion_interactividad(data)
    datos = puntuacion_representacion_datos(data)
    data = [condicionales, sincronizacion, flujo, abstraccion, paralelismo, categoria, interactividad, datos]
    media = mean(data)
    puntuacion = switch_puntuacion(media)
    level = switch_nivel.get(puntuacion)
    lista_to_csv = [name_project, file_xml, level, puntuacion, media]
    lista_to_csv.extend(data)
    #print(file_xml)
    #if len(lista_to_csv):
        #print(*[item for item in lista_to_csv], sep=',')
    return lista_to_csv
