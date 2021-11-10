"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
UFOSfile = 'UFOS-utf8-small.csv'
cont = None


def printMenu():
    print("Bienvenido")
    print("0- Salir del programa")
    print("1- Inicializar Analizador")
    print("2- Cargar información en el catálogo")
    print("3- Contar los avistamientos en una ciudad")
    print("4- Contar los avistamientos por duración")
    print("5- Contar avistamientos por Hora/Minutos del día")
    print("6- Contar los avistamientos en un rango de fechas")
    print("7- Contar los avistamientos de una Zona Geográfica")
    print("8-  Visualizar los avistamientos de una zona geográfica.")

catalog = None

"""
Menu principal
"""
def printPrimerosUFOS(analyzer):
    print('Los primeros 5 Avistamientos de UFOS son: \n')
    avistamientos = analyzer['Avistamientos']
    i=1
    while i in range (1,6):
        avistamiento = lt.getElement(avistamientos,i)
        print('Fecha: ' + avistamiento['datetime'] +", Ciudad: " + avistamiento['city'] +', Pais: ' + avistamiento['country']+ ', Forma: '+ avistamiento['shape']+', Duracion(segundos): '+avistamiento['duration (seconds)'])
        i+=1
    pass

def printUltimosUFOS(analyzer):
    print('Los ultimos 5 Avistamientos de UFOS son: \n')
    avistamientos = analyzer['Avistamientos']
    size = lt.size(avistamientos)
    i = size
    while i in range (size-4, size+1):
        avistamiento = lt.getElement(avistamientos,i)
        print('Fecha: ' + avistamiento['datetime'] +", Ciudad: " + avistamiento['city'] +', Pais: ' + avistamiento['country']+', Forma: '+ avistamiento['shape']+', Duracion(segundos): '+avistamiento['duration (seconds)'])
        i-=1
    pass

def printDuration(lista):
    for element in lt.iterator(lista):
        print("Fecha y hora: " + element["datetime"] + ", Ciudad: " + element['city'] +', Pais: ' + element['country'] + ", Duracion en Segundos: " + element["duration (seconds)"] + ", Forma del Objeto: " +element["shape"] + ", Longitud: " +element["longitude"] + ", Latitud: " +element["latitude"])

def printCoordinates(lista):
    for element in lt.iterator(lista):
        print("Fecha y hora: " + element["datetime"] + ", Ciudad: " + element['city'] +', Pais: ' + element['country'] + ", Duracion en Segundos: " + element["duration (seconds)"] + ", Forma del Objeto: " +element["shape"])


def printPrimeros3(lista):
    i=1
    while i in range (1,4):
        avistamiento = lt.getElement(lista,i)
        print('Fecha: ' + avistamiento['datetime'] +", Ciudad: " + avistamiento['city'] +', Pais: ' + avistamiento['country']+ ', Forma: '+ avistamiento['shape']+', Duracion(segundos): '+avistamiento['duration (seconds)'])
        i+=1
    pass

def printUltimos3(lista):
    size = lt.size(lista)
    i = size
    while i in range (size-2, size+1):
        avistamiento = lt.getElement(lista,i)
        print('Fecha: ' + avistamiento['datetime'] +", Ciudad: " + avistamiento['city'] +', Pais: ' + avistamiento['country']+', Forma: '+ avistamiento['shape']+', Duracion(segundos): '+avistamiento['duration (seconds)'])
        i-=1
    pass



while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()
    elif int(inputs[0]) == 2:
        print("Cargando información de los archivos ....")
        controller.loadData(cont,UFOSfile)
        print('UFOS cargados: ' + str(controller.UFOSSize(cont)))
        printPrimerosUFOS(cont)
        printUltimosUFOS(cont)

    elif int(inputs[0]) == 3:
        ciudad = input("Por favor indique la ciudad en la cual quiere hacer la búsqueda: ")
        print("La ciudad que eligió tiene un total de " + str(controller.FindCity(cont, ciudad)[2])+ " avistamientos")
        primeros3 = controller.FindCity(cont, ciudad)[0]
        ultimos3 = controller.FindCity(cont, ciudad)[1]
        print("Entre estos, se encuentran los primeros tres (ordenados según su fecha de observación):")
        printDuration(primeros3)
        print("Y los últimos tres (ordenados según su fecha de observación):")
        printDuration(ultimos3)
        """print('Altura del arbol: ' + str(controller.indexAltura(cont)))
        print('Elementos en el arbol: ' + str(controller.indexSize(cont)))
        print('Llave mayor: ' + str(controller.maxKey(cont)))
        print('Llave menor: ' + str(controller.minKey(cont)))"""

    elif int(inputs[0]) == 4:
        second1 = float(input("Porfavor seleccione la cantidad de segundos con la cual desea iniciar el rango: "))
        second2 = float(input("Porfavor seleccione la cantidad de segundos con la cual desea finalizar el rango: "))
        lista_llaves = controller.RangoDuracion(cont, second1, second2)
        print("La duración máxima (en segundos) fue de : " + str(controller.maxKeySeconds(cont)) + " segundos. \nEsta duración la tuvieron " + str(controller.SizeMaxKeySeconds(cont)) + " avistamientos.")
        tupla = controller.getMin3yMax3(cont, second1, second2)
        primeras_llaves = tupla[0]
        ultimas_llaves = tupla[1]
        min3 = controller.getMin3(cont, primeras_llaves)
        max3 = controller.getMax3(cont, ultimas_llaves)
        print("Los primeros 3 avistamenientos dentro del rango son: ")
        printDuration(min3)
        print("---*50")
        print("Los últimos 3 avistamientos dento del rango son:")
        printDuration(max3)
    elif int(inputs[0]) == 5:
        pass
    elif int(inputs[0]) == 6:
        fecha_1=input('Limite inferior (AAAA-MM-DD): ')
        fecha_2=input('Limite superior (AAAA-MM-DD): ')
        print('\nSe encontraron ' + str(controller.indexSize(cont)) + ' avistamientos con distintas fechas')
        result = controller.BuscarEnRangoDeFechas(cont['dateIndex'], fecha_1, fecha_2)
        minimo= controller.encontrarMinimo(cont['dateIndex'])
        print('El avistamiento mas antiguo fue en: ' + str(minimo[0]))
        print('Numero de avistamientos del dia del avistamiento más antiguo : ' + str(minimo[1]))
        print('\nSe encontraron ' + str(result[0]) + ' avistamientos en el rango')
        print('\nPimeros 3 avistamientos del rango:')
        printPrimeros3(result[1])
        print('\nUltimos 3 avistamientos del rango:')
        printUltimos3(result[1])
    elif int(inputs[0]) == 7:
        longitud1 = float(input("Por favor seleccione el límite inferior de sus longitudes aproximado a dos cifras decimales"))
        longitud2 = float(input("Por favor seleccione el límite superior de sus longitudes aproximado a dos cifras decimales"))
        latitud1 = float(input("Por favor seleccione el límite inferior de sus latitudes aproximado a dos cifras decimales"))
        latitud2 = float(input("Por favor seleccione el límite inferior de sus latitudes aproximado a dos cifras decimales"))
        lista_todas = controller.ConseguirTodasEnRangoCoordenadas(cont, longitud1, longitud2, latitud1, latitud2)
        printCoordinates(lista_todas)
    elif int(inputs[0]) == 8:
        pass
    else:
        sys.exit(0)
sys.exit(0)
