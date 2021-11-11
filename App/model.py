"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf
import datetime

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newAnalyzer():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los crimenes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas

    Retorna el analizador inicializado.
    """
    analyzer = {'Avistamientos': None,
                'ciudadIndex': None
                }

    analyzer['Avistamientos'] = lt.newList('SINGLE_LINKED', compareDates)
    analyzer['ciudadIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    analyzer["duration_seconds"] = om.newMap(omaptype='RBT',
                                      comparefunction=compareSeconds)
    analyzer["coordinates"] = om.newMap(omaptype='RBT',
                                      comparefunction=compareSeconds)
    analyzer['dateIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    analyzer['timeIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    return analyzer
# Funciones para agregar informacion al catalogo
def addUFO(analyzer, UFO):
    lt.addLast(analyzer['Avistamientos'], UFO)
    updateCiudadIndex(analyzer['ciudadIndex'], UFO)
    updateSegundosIndex(analyzer["duration_seconds"], UFO)
    updateCoordinatesIndex(analyzer["coordinates"], UFO)
    updatedateIndex(analyzer['dateIndex'],UFO)
    updatetimeIndex(analyzer['timeIndex'],UFO)
    return analyzer

# Funciones para MAP Req 1 (David)
def updateCiudadIndex(map, UFO):
    ciudad = UFO['city']
    entrada = om.get(map, ciudad)
    if entrada is None:
        entrada_ciudad = NewCityEntry(UFO)
        om.put(map, ciudad, entrada_ciudad)
    else:
        entrada_ciudad = me.getValue(entrada)
        addCiudadIndex(entrada_ciudad, UFO)
    return map

def NewCityEntry(UFO):
    entrada = {'FirstUFO': None}
    entrada['FirstUFO'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareNames)
    first = entrada['FirstUFO']
    occurreddate = UFO["datetime"]
    crimedate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    om.put(first, crimedate.date(), UFO)
    return entrada

def addCiudadIndex(entrada_ciudad, UFO):
    first = entrada_ciudad['FirstUFO']
    occurreddate = UFO["datetime"]
    crimedate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    om.put(first, crimedate.date(), UFO)
    return entrada_ciudad

#Funciones de consulta Req 1 (David)
def FindCity(analyzer, ciudad):
    mapa = analyzer["ciudadIndex"]
    entrada = om.get(mapa, ciudad)
    entrada_ciudad = me.getValue(entrada)
    nuevo_mapa = entrada_ciudad["FirstUFO"]
    tamano = om.size(nuevo_mapa)
    valores = om.valueSet(nuevo_mapa)
    primeras3 = lt.subList(valores, 1, 3)
    ultimas3 = lt.subList(valores, lt.size(valores)-2, 3)
    return primeras3, ultimas3, tamano

def FindTopCity(analyzer):
    mapa = analyzer["ciudadIndex"]
    llaves = om.keySet(mapa)
    contador = 0 
    mayor = ""
    for llave in lt.iterator(llaves):
        entrada = om.get(mapa, llave)
        entrada_ciudad = me.getValue(entrada)
        nuevo_mapa = entrada_ciudad["FirstUFO"]
        tamano = om.size(nuevo_mapa)
        if tamano >= contador:
            contador = tamano
            mayor = llave
    return mayor, contador


#Funciones para MAP Req 2 (David)
def updateSegundosIndex(map, UFO):
    segundos = float(UFO["duration (seconds)"])
    entrada = om.get(map, segundos)
    if entrada is None:
        entrada_segundos = NewSecondsEntry(UFO)
        om.put(map, segundos, entrada_segundos)
    else:
        entrada_segundos = me.getValue(entrada)
        addSecondsIndex(entrada_segundos, UFO)
    return map

def NewSecondsEntry(UFO):
    entrada = {"FirstUFO": None}
    entrada["FirstUFO"] = om.newMap(omaptype='RBT',
                                      comparefunction=compareNames)
    first = entrada['FirstUFO']
    om.put(first, UFO["city"], UFO)
    return entrada

def addSecondsIndex(entrada_ciudad, UFO):
    first = entrada_ciudad["FirstUFO"]
    om.put(first, UFO["city"], UFO)
    return entrada_ciudad

#Funciones de consulta Req 2 (David)


def maxKeySeconds(analyzer):
    return om.maxKey(analyzer['duration_seconds'])

def SizeMaxKeySeconds(analyzer):
    llave = maxKeySeconds(analyzer)
    entry = om.get(analyzer["duration_seconds"], llave)
    dicc = me.getValue(entry)
    mapa = dicc["FirstUFO"]
    return om.size(mapa)

def getMin3yMax3(analyzer, second1, second2):
    mapa = analyzer["duration_seconds"]
    lista = RangoDuracion(analyzer, second1, second2)
    primeros3 = lt.subList(lista, 1, 3)
    ultimos3 = lt.subList(lista, lt.size(lista)-2, 3)
    return primeros3, ultimos3

def SizeKey(analyzer, llave):
    entry = om.get(analyzer["duration_seconds"], llave)
    dicc = me.getValue(entry)
    mapa = dicc["FirstUFO"]
    return om.size(mapa)


def getMin3(analyzer, primeras_llaves):
    lista = lt.newList(cmpfunction=compareNames)
    #para primera llave
    llave1 = lt.getElement(primeras_llaves, 1)
    entry1 = om.get(analyzer["duration_seconds"], llave1)
    dicc1 = me.getValue(entry1)
    mapa1 = dicc1["FirstUFO"]
    valores1 = om.valueSet(mapa1)
    for element in lt.iterator(valores1):
        lt.addLast(lista, element)
    #para segunda llave
    llave2 = lt.getElement(primeras_llaves, 2)
    entry2 = om.get(analyzer["duration_seconds"], llave2)
    dicc2 = me.getValue(entry2)
    mapa2 = dicc2["FirstUFO"]
    valores2 = om.valueSet(mapa2)
    for element in lt.iterator(valores2):
        lt.addLast(lista, element)
    #para tercera llave
    llave3 = lt.getElement(primeras_llaves, 3)
    entry3 = om.get(analyzer["duration_seconds"], llave3)
    dicc3 = me.getValue(entry3)
    mapa3 = dicc3["FirstUFO"]
    valores3 = om.valueSet(mapa3)
    for element in lt.iterator(valores3):
        lt.addLast(lista, element)
    min3 = lt.subList(lista, 1, 3)
    return min3

def getMax3(analyzer, ultimas_llaves):
    lista = lt.newList(cmpfunction=compareNames)
    #para primera llave
    llave1 = lt.getElement(ultimas_llaves, 1)
    entry1 = om.get(analyzer["duration_seconds"], llave1)
    dicc1 = me.getValue(entry1)
    mapa1 = dicc1["FirstUFO"]
    valores1 = om.valueSet(mapa1)
    for element in lt.iterator(valores1):
        lt.addLast(lista, element)
    #para segunda llave
    llave2 = lt.getElement(ultimas_llaves, 2)
    entry2 = om.get(analyzer["duration_seconds"], llave2)
    dicc2 = me.getValue(entry2)
    mapa2 = dicc2["FirstUFO"]
    valores2 = om.valueSet(mapa2)
    for element in lt.iterator(valores2):
        lt.addLast(lista, element)
    #para tercera llave
    llave3 = lt.getElement(ultimas_llaves, 3)
    entry3 = om.get(analyzer["duration_seconds"], llave3)
    dicc3 = me.getValue(entry3)
    mapa3 = dicc3["FirstUFO"]
    valores3 = om.valueSet(mapa3)
    for element in lt.iterator(valores3):
        lt.addLast(lista, element)
    max3 = lt.subList(lista, lt.size(lista)-2, 3)
    return max3   

def RangoDuracion(analyzer, second1, second2):
    mapa = analyzer["duration_seconds"]
    lista = om.keys(mapa, second1, second2)
    return lista

#Funciones req 3
def updatetimeIndex(map, UFO):
    date1 = UFO['datetime']
    datetm1= datetime.datetime.strptime(date1, '%Y-%m-%d %H:%M:%S')
    time = datetm1.time()
    entry = om.get(map, time)
    if entry is None:
        dateentry = newDateEntry(UFO)
        om.put(map, time, dateentry)
    else:
        dateentry = me.getValue(entry)
        addCityIndex(dateentry, UFO)
    return map

    

def BuscarEnRangoDeHoras(cont, fecha_1, fecha_2):
    Datein= datetime.datetime.strptime(fecha_1, '%H:%M:%S')
    fechain=Datein.time()
    Datefin= datetime.datetime.strptime(fecha_2, '%H:%M:%S')
    fechafin=Datefin.time()
    valores= om.values(cont, fechain, fechafin)
    contador=0
    primera_entrada= lt.newList("ARRAY_LIST")
    for primeros_valores in lt.iterator(valores):
        contador += primeros_valores['cuenta']
        for ufo in lt.iterator(primeros_valores['FirstUFO']):
            lt.addLast(primera_entrada, ufo)
    return contador, primera_entrada
#Funciones req 4
def updatedateIndex(map, UFO):
    date1 = UFO['datetime']
    datetm1= datetime.datetime.strptime(date1, '%Y-%m-%d %H:%M:%S')
    date = datetm1.date()
    entry = om.get(map, date)
    if entry is None:
        dateentry = newDateEntry(UFO)
        om.put(map, date, dateentry)
    else:
        dateentry = me.getValue(entry)
        addCityIndex(dateentry, UFO)
    return map



def newDateEntry(UFO):
    entry = {'FirstUFO': None, 'cuenta':0}
    entry['FirstUFO'] = lt.newList('ARRAY_LIST', compareDates)
    First = entry['FirstUFO']
    lt.addLast(First, UFO)
    entry['cuenta']+= 1
    return entry
def addCityIndex(entrada_ciudad, UFO):
    first= entrada_ciudad['FirstUFO']
    lt.addLast(first,UFO)
    entrada_ciudad['cuenta']+=1
    return entrada_ciudad


def BuscarEnRangoDeFechas(cont, fecha_1, fecha_2):
    Datein= datetime.datetime.strptime(fecha_1, '%Y-%m-%d')
    fechain=Datein.date()
    Datefin= datetime.datetime.strptime(fecha_2, '%Y-%m-%d')
    fechafin=Datefin.date()
    valores= om.values(cont, fechain, fechafin)
    contador=0
    primera_entrada= lt.newList("ARRAY_LIST")
    for primeros_valores in lt.iterator(valores):
        contador += primeros_valores['cuenta']
        for ufo in lt.iterator(primeros_valores['FirstUFO']):
            lt.addLast(primera_entrada, ufo)
    ultimos3 = lt.subList(primera_entrada, lt.size(primera_entrada)-2, 3)
    return contador, primera_entrada, ultimos3

def encontrarMinimo(analyzer):
    llavemin = om.minKey(analyzer)
    entradamin = om.get(analyzer,llavemin)
    contador=lt.size(entradamin)

    return llavemin , contador



#Funciones para MAP Req 5 (David)
def updateCoordinatesIndex(map, UFO):
    longitud = round(float(UFO["longitude"]), 2)
    entrada = om.get(map, longitud)
    if entrada is None:
        entrada_longitud = NewLongitudEntry(UFO)
        om.put(map, longitud, entrada_longitud)
    else:
        entrada_longitud = me.getValue(entrada)
        addLongitudIndex(entrada_longitud, UFO)
    return map
#Crea el mapa nuevo en caso de que la longitud no exista aún    
def NewLongitudEntry(UFO):
    entrada = {"FirstUFO": None}
    entrada["FirstUFO"] = om.newMap(omaptype='RBT',
                                      comparefunction=compareNames)
    map = entrada["FirstUFO"]
    latitud = round(float(UFO["latitude"]), 2)
    entrada1 = om.get(map, latitud)
    if entrada1 is None:
        entrada_latitud = NewLatitudeEntry(UFO)
        om.put(map, latitud, entrada_latitud)
    else:
        entrada_latitud = me.getValue(entrada)
        addLatitudIndex(entrada_latitud, UFO)
    return entrada

def NewLatitudeEntry(UFO):
    entrada = {'FirstUFO': None}
    entrada['FirstUFO'] = lt.newList('ARRAY_LIST', compareDates)
    first = entrada['FirstUFO']
    lt.addLast(first, UFO)
    return entrada
def addLatitudIndex(entrada_latitud, UFO):
    first = entrada_latitud['FirstUFO']
    lt.addLast(first, UFO)
    return entrada_latitud

def addLongitudIndex(entrada_longitud, UFO):
    first = entrada_longitud["FirstUFO"]
    latitud = round(float(UFO["latitude"]), 2)
    entrada = om.get(first, latitud)
    if entrada is None:
        entrada_latitud = NewLatitudeEntry(UFO)
        om.put(first, latitud, entrada_latitud)
    else:
        entrada_latitud = me.getValue(entrada)
        addLatitudIndex(entrada_latitud, UFO)
    return entrada_longitud

#Funciones de consulta Req 5 (David)

def ConseguirTodasEnRangoCoordenadas(analyzer, longitud1, longitud2, latitud1, latitud2):
    gran_lista = lt.newList(cmpfunction=compareNames)
    mapa = analyzer["coordinates"]
    lista_longitud = om.keys(mapa, longitud1, longitud2)
    print(lista_longitud)
    for llave in lt.iterator(lista_longitud):
        entry = om.get(mapa, llave)
        dicc = me.getValue(entry)
        mapa_latitudes = dicc["FirstUFO"]
        lista_latitudes = om.keys(mapa_latitudes, latitud1, latitud2)
        for llave1 in lt.iterator(lista_latitudes):
            entry = om.get(mapa_latitudes, llave1)
            dicc1 = me.getValue(entry)
            lista_ufo = dicc1["FirstUFO"]
            for element in lt.iterator(lista_ufo):
                lt.addLast(gran_lista, element)
    return gran_lista





# Funciones de consulta
def indexAltura(analyzer):
    return om.height(analyzer['ciudadIndex'])


def indexSize(analyzer):
    return om.size(analyzer)


def minKey(analyzer):
    return om.minKey(analyzer['ciudadIndex'])


def maxKey(analyzer):
    return om.maxKey(analyzer['ciudadIndex'])

def UFOSSize(analyzer):
    return lt.size(analyzer["Avistamientos"])
# Funciones utilizadas para comparar elementos dentro de una lista
def compareDates(date1, date2):
    
    if (date1 > date2):
        return 1
    elif (date1 == date2):
        return 0
    else:
        return -1

def compareSeconds(second1, second2):
    if (second1 > second2):
        return 1
    elif (second1 == second2):
        return 0
    else:
        return -1

def compareNames(name1, name2):
    if (name1>name2):
        return 1
    elif name1==name2:
        return 0
    else:
        return -1
# Funciones de ordenamiento



horain= datetime.datetime.strptime("1900-05-02 20:45:00", '%Y-%m-%d %H:%M:%S')
fechain= horain.time()
horafin= datetime.datetime.strptime("1900-05-02 20:55:00", '%Y-%m-%d %H:%M:%S')
fechafin= horafin.time()
boool=fechain<fechafin
print(boool)