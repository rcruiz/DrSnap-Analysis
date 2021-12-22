import json
import os
from statistics import mean, mode
from parser import ParserXML
from collections import Counter

PATH_JSON_SNAP_PROJECT = os.path.dirname(os.path.abspath(__file__)) + '/' + 'data.json'


def blocks_script(data):
    previous_flag = 0
    result = False
    for element in data['sprites']:
        current_flag = element['script']
        if previous_flag == current_flag:
            result = True
            break
        else:
            previous_flag = element['script']
    return result


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
    score = 0
    parallelism_counter = 0
    list_scores = []
    n_script = number_script(data)
    n_sprite = number_sprite(data)
    basic = n_sprite == 1 and n_script >= 2
    intermediate = n_sprite >= 2 and n_script >= 1
    list_score_3 = ['receiveCondition', 'receiveMessage', 'receiveOnClone']
    for element in data['sprites']:
        # receive_go_key = element['block'] == 'receiveGo' or element['block'] == 'receiveKey'
        # evaluate y assign :=
        if (receive_go_key := element['block'] == 'receiveGo' or element['block'] == 'receiveKey') and basic:
            score = 1
        elif receive_go_key and intermediate:
            score = 2
        elif element['block'] in list_score_3:
            score = 3
            # break
        list_scores.append(score)
    if list_scores:
        parallelism_counter = Counter(list_scores).most_common()[0][0]
    # return parallelism_counter
    return score


def puntuacion(data, switch):
    mayor = 0
    for element in data['sprites']:
        actual = switch.get(element['block'])
        if actual is not None and mayor < actual:
            mayor = actual
            if mayor == 3:
                # mayor puntuacion no hace falta buscar mas
                break
    # moda = mode(actual)
    return mayor


def puntuacion_condicionales(data):
    switch_conditionals = {
        'doIf': 1,
        'doIfElse': 2,
        'reportIfElse': 2,
        'reportAnd': 3,
        'reportOr': 3,
        'reportNot': 3
    }
    list_scores = [switch_conditionals.get(element['block']) for element in data['sprites'] if
                   switch_conditionals.get(element['block']) is not None]
    count_scores = Counter(list_scores)
    score2 = len(count_scores)
    # Other method calculate conditionals.
    if count_scores[3] and count_scores[2] and count_scores[1]:
        score = 3
    elif count_scores[3] and count_scores[2] or count_scores[3] and count_scores[1] or count_scores[2] and count_scores[1]:
        score = 2
    elif count_scores[3] or count_scores[2] or count_scores[1]:
        score = 1
    else:
        score = 0
    return score2


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
        "doDeleteAttr": 2,
        "doSetVar": 2,
        "doChangeVar": 2,
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
    return puntuacion(data, switch_datos)


def puntuacion_interactividad(data):
    switch_interactividad = {
        "receiveGo": 1,
        "receiveKey": 1,
        "receiveInteraction": 1,
        "reportKeyPressed": 1,
        "doAsk": 2,  # la mayoria
        "getLastAnswer": 2,
        "reportTouchingObject": 2,
        "reportMouseDown": 2,
        "reportTouchingColor": 3,
        "reportColorIsTouchingColor": 3,
        "doSetVideoTransparency": 3,
        "reportVideo": 3,
        "doSetGlobalFlag": 3,
        "reportGlobalFlag": 3,
        "reportAudio": 3
    }
    return puntuacion(data, switch_interactividad)


def puntuacion_sincronizacion(data):
    switch_sincronizacion = {
        "doWait": 1,
        "doBroadcast": 2,
        "receiveMessage": 2,
        "doStopThis": 2,
        "doPauseAll": 2,
        "doWaitUntil": 3,
        "reportAskFor": 3,
        "doBroadcastAndWait": 3,
        "receiveCondition": 3,
        'receiveOnClone': 3
    }
    return puntuacion(data, switch_sincronizacion)


def control_flujo(data):
    switch_flujo = {
        'doForever': 2,
        'doRepeat': 2,
        'for': 2,
        'doWaitUntil': 3,
        'doUntil': 3
    }
    puntuacion_bajo = 0
    # Check if the scripts has 2 or more blocks that are executed sequentially.
    resultado = blocks_script(data)
    if resultado:
        puntuacion_bajo = 1
    mayor = puntuacion(data, switch_flujo)
    return max(puntuacion_bajo, mayor)


def puntuacion_abstraccion(data):
    n_script = number_script(data)
    n_sprite = number_sprite(data)
    count_type_blocks = Counter(element["block"] for element in data['sprites'])
    clones = count_type_blocks.get("createClone")
    # list_clones = [sprite["block"].count("createClone") for sprite in data["sprites"] if
    #                  sprite["block"] == "createClone"]
    cond_scripts = n_sprite > 1 and n_script > 1
    conditions = [data['block-definition'], clones, cond_scripts]
    # evaluate_conditions = sum(map(bool, conditions)) # Assign score from verified conditions.
    # if all(conditions):
    if data['block-definition'] and clones and cond_scripts:
        score = 3
    # elif sum(map(bool, conditions)) == 2:
    # elif not all(conditions) and any(conditions): # 1 or 2 conditions.
    elif data["block-definition"] and clones or data["block-definition"] and cond_scripts or cond_scripts and clones:
        score = 2
    # elif sum(map(bool, conditions)) == 1:
    elif data['block-definition'] or clones or cond_scripts: # (cond_scripts := n_sprite > 1 and n_script > 1):
        score = 1
    else:
        score = 0
    return score


def calcular_level_total(data):
    total = sum(data)
    if total <= 7:
        level = "Basic"
    elif 7 < total <= 14:
        level = "Intermediate"
    else:
        level = "Advanced"
    return level, total


def calcular_puntuacion(file_xml):
    ParserXML(file_xml)
    with open(PATH_JSON_SNAP_PROJECT) as file:
        data = json.load(file)
    name_project = (data['project_name'][0]['name']).strip(" \r\n").replace("\r", " ")
    condicionales = puntuacion_condicionales(data)
    sincronizacion = puntuacion_sincronizacion(data)
    flujo = control_flujo(data)
    abstraccion = puntuacion_abstraccion(data)
    paralelismo = puntuacion_paralelismo(data)
    interactividad = puntuacion_interactividad(data)
    datos = puntuacion_representacion_datos(data)
    ct_scores = [condicionales, sincronizacion, flujo, abstraccion, paralelismo, interactividad, datos]
    level, total = calcular_level_total(ct_scores)
    average = mean(ct_scores)
    list_to_csv = [name_project, file_xml, level, total, average]
    list_to_csv.extend(ct_scores)
    return list_to_csv
