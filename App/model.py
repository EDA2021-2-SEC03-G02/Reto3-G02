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
    return analyzer
# Funciones para agregar informacion al catalogo
def addUFO(analyzer, UFO):
    lt.addLast(analyzer['Avistamientos'], UFO)
    updateCiudadIndex(analyzer['ciudadIndex'], UFO)
    updateSegundosIndex(analyzer["duration_seconds"], UFO)
    return analyzer

def updateCiudadIndex(map, UFO):
    ciudad = UFO['city']
    entrada = om.get(map, ciudad)
    if entrada is None:
        entrada_ciudad = NewDataEntry(UFO)
        om.put(map, ciudad, entrada_ciudad)
    else:
        entrada_ciudad = me.getValue(entrada)
        addCiudadIndex(entrada_ciudad, UFO)
    return map

def NewDataEntry(UFO):
    entrada = {'FirstUFO': None}
    entrada['FirstUFO'] = lt.newList('ARRAY_LIST', compareDates)
    first = entrada['FirstUFO']
    lt.addLast(first, UFO)
    return entrada

def addCiudadIndex(entrada_ciudad, UFO):
    first = entrada_ciudad['FirstUFO']
    lt.addLast(first, UFO)
    return entrada_ciudad


#Funciones Req 2 (David)
def updateSegundosIndex(map, UFO):
    segundos = UFO["duration (seconds)"]
    entrada = om.get(map, segundos)
    if entrada is None:
        None


# Funciones para creacion de datos

# Funciones de consulta
def indexAltura(analyzer):
    return om.height(analyzer['ciudadIndex'])


def indexSize(analyzer):
    return om.size(analyzer['ciudadIndex'])


def minKey(analyzer):
    return om.minKey(analyzer['ciudadIndex'])


def maxKey(analyzer):
    return om.maxKey(analyzer['ciudadIndex'])

def UFOSSize(analyzer):
    return lt.size(analyzer['Avistamientos'])
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
# Funciones de ordenamiento
