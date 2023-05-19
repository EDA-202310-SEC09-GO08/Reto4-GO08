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
import model
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf
from tabulate import tabulate
import traceback
from DISClib.ADT import graph as gr
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
            
            size ='BA-Grey-Wolf-tracks-utf8-5pct.csv'
            return size
        elif int(porcentaje) == 3:
            size = 'BA-Grey-Wolf-tracks-utf8-10pct.csv'
            return size
        elif int(porcentaje) == 4:
            size = 'BA-Grey-Wolf-tracks-utf8-20pct.csv'
            return size
        elif int(porcentaje) == 5:
            size = 'BA-Grey-Wolf-tracks-utf8-30pct.csv'
            return size
        elif int(porcentaje) == 6:
            size = 'BA-Grey-Wolf-tracks-utf8-50pct.csv'
            return size
        elif int(porcentaje) == 1:
            size = 'BA-Grey-Wolf-tracks-utf8-small.csv'
            lobos='BA-Grey-Wolf-individuals-utf8-small.csv'
            return size,lobos
        elif int(porcentaje) == 7:
            size = 'BA-Grey-Wolf-tracks-utf8-80pct.csv'
            return size
        elif int(porcentaje) == 8:
            size = 'BA-Grey-Wolf-tracks-utf8-large.csv'
            return size,lobos
    except ValueError:
            print(" una opción válida.\n")
            traceback.print_exc()


def load_data_tracks(control,size):
    """
    Carga los datos
    """
    control =controller.load_data(control,size)
    return control

def load_data_wolfs(control,size):
    """
    Carga los datos
    """
    control =controller.load_data_2(control,size)
    return control

def calc_eventos_filt_hay(control):
    ds=control['model']
    mapa =ds['mapa lobos']
    lobos =lt.iterator(mp.keySet(mapa))
    j=0
    for lobo in lobos:
        size =lt.size(model.devolver_value(mapa,lobo))

        j+=size

    return j

def print_carga_datos():
    dos_archivos = menu_archivo()
    archivo_tracks=dos_archivos[0]
    archivo_lobos=dos_archivos[1]
    control = new_controller()
    load_data_tracks(control,archivo_tracks)
    load_data_wolfs(control,archivo_lobos)

    data_structs=control['model']

    ### WOLF AND event features

    print('---------WOLFS AND EVENTS FEATURES------------ ')
    print('')
    print('')
    n_wolf=lt.size(data_structs['lista archivo lobos'])
    n_WW_data= mp.size(data_structs['mapa lobos'])
    n_events=lt.size(data_structs['lista total'])
    print('Number of wolfs: '+str(n_wolf))
    print('Number of wolfs with data: '+str(n_WW_data))
    print('number of events: '+str(n_events))

    ### NODES FEATURES

    print('---------NODES FEATURES------------ ')
    print('')
    print('')
    n_gathering=mp.size(data_structs['mapa nodos de encuentro'])
    n_track= mp.size(data_structs['mapa nodos de seguimiento'])
    n_nodes=n_track+n_gathering
    print('Number of gathering points: '+str(n_gathering))
    print('Number of tracking points '+str(n_track))
    print('Total nodes: '+str(n_nodes))
    print(n_nodes)


    ### EDGE FEATURES
    n_edges=gr.numEdges(data_structs['grafo'])
    print(n_edges)
    print(data_structs['n arcos de seguimiento'])
    print('eventos filt')
    print(calc_eventos_filt_hay(control))



    #print('nodos seguimiento: '+str(size))
    #print('primeros')
    #print(lt.getElement(lista_nodos,1))
    #print(lt.getElement(lista_nodos,2))
    #print(lt.getElement(lista_nodos,3))
    #print(lt.getElement(lista_nodos,4))
    #print(lt.getElement(lista_nodos,5))

    #print('ultimos')
    #print(lt.getElement(lista_nodos,size-1))
    #print(lt.getElement(lista_nodos,size-2))
    #print(lt.getElement(lista_nodos,size-3))
    #print(lt.getElement(lista_nodos,size-4))
    #print(lt.getElement(lista_nodos,size-5))      
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
                print_carga_datos()

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
