﻿"""
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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # catalog es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer
# Funciones para la carga de datos
def loadData(analyzer, UFOSfile):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    UFOSfile = cf.data_dir + UFOSfile
    input_file = csv.DictReader(open(UFOSfile, encoding="utf-8"),
                                delimiter=",")
    for UFO in input_file:
        model.addUFO(analyzer, UFO)
    return analyzer
# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def UFOSSize(analyzer):
    """
    Numero de crimenes leidos
    """
    return model.UFOSSize(analyzer)


def indexAltura(analyzer):
    """
    Altura del indice (arbol)
    """
    return model.indexAltura(analyzer)


def indexSize(analyzer):
    """
    Numero de nodos en el arbol
    """
    return model.indexSize(analyzer)


def minKey(analyzer):
    """
    La menor llave del arbol
    """
    return model.minKey(analyzer)


def maxKey(analyzer):
    """
    La mayor llave del arbol
    """
    return model.maxKey(analyzer)