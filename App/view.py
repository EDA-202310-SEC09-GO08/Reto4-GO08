﻿"""
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
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf
from tabulate import tabulate
import traceback

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    control = controller.new_controller()

    return control

def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- REQ. 1: Planear una posible ruta entre dos puntos de encuentro (G)")
    print("3- REQ. 2: Planear una ruta con menos paradas entre dos puntos de encuentro (G)")
    print("4- REQ. 3: Reconocer los territorios habitados por distintas manadas (I)")
    print("5- REQ. 4: Identificar el camino más corto entre dos puntos del hábitat (I)")
    print("6- REQ. 5: Reconocer el coredor migratorio mas extenso (I)")
    print("7- REQ. 6: Identificar diferencias de movilidad entre tipos de miembros de la manada (G)")
    print("8- REQ. 7: Identificar cambios en el territorio de las manadas según condiciones climáticas (G)")
    print("9- REQ. 8: Graficar resultados para cada uno de los requerimientos (B)")
    print("0- Salir")


def menu_nombre_archivo():
    print("Que porcentage de datos ")
    print("1-1%")
    print("2-5%")
    print("3-10%")
    print("4-20%")
    print("5-30%")
    print("6-50%")
    print("7-80%")
    print("8-100%")

def menu_archivo():
    menu_nombre_archivo()
    porcentaje = input('Seleccione una opción para continuar\n')
    try:
        if int(porcentaje) == 2:
            
            size ='datos_siniestralidad-5pct.csv'
            return size
        elif int(porcentaje) == 3:
            size = 'datos_siniestralidad-10pct.csv'
            return size
        elif int(porcentaje) == 4:
            size = 'datos_siniestralidad-20pct.csv'
            return size
        elif int(porcentaje) == 5:
            size = 'datos_siniestralidad-30pct.csv'
            return size
        elif int(porcentaje) == 6:
            size = 'datos_siniestralidad-50pct.csv'
            return size
        elif int(porcentaje) == 1:
            size = 'BA-Grey-Wolf-tracks-utf8-small.csv'
            return size
        elif int(porcentaje) == 7:
            size = 'datos_siniestralidad-80pct.csv'
            return size
        elif int(porcentaje) == 8:
            size = 'datos_siniestralidad-large.csv'
            return size
    except ValueError:
            print(" una opción válida.\n")
            traceback.print_exc()
def load_data(control,size):
    """
    Carga los datos
    """
    control =controller.load_data(control,size)
    return control


def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    pass


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    pass


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    pass


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    pass


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    pass


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    pass


def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    pass


def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass


# Se crea el controlador asociado a la vista
control = new_controller()

# main del reto
if __name__ == "__main__":
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        try:
            if int(inputs) == 1:
                print("Cargando información de los archivos ....\n")
                size = menu_archivo()
                control = new_controller()
                data = load_data(control,size)
                print(data[1])
            elif int(inputs) == 2:
                print_req_1(control)

            elif int(inputs) == 3:
                print_req_2(control)

            elif int(inputs) == 4:
                print_req_3(control)

            elif int(inputs) == 5:
                print_req_4(control)

            elif int(inputs) == 6:
                print_req_5(control)

            elif int(inputs) == 7:
                print_req_6(control)

            elif int(inputs) == 8:
                print_req_7(control)

            elif int(inputs) == 9:
                print_req_8(control)

            elif int(inputs) == 0:
                working = False
                print("\nGracias por utilizar el programa")
                
            else:
                print("Opción errónea, vuelva a elegir.\n")
        except Exception as exp:
            print("ERR:", exp)
            traceback.print_exc()
    sys.exit(0)
