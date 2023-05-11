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
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.ADT import minpq as mpq
from DISClib.ADT import indexminpq as impq
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import graph as gr
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import bellmanford as bf
from DISClib.Algorithms.Graphs import bfs
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import prim
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import mergesort as merg
from DISClib.Algorithms.Sorting import quicksort as quk
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos


def new_data_structs():
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    data_structs ={}
    data_structs['lista total']=lt.newList(datastructure='ARRAY_LIST')



#### mapa cuya llave es un lobo en id y el valor es el array de los eventos seguidos por el dicho lobo (ordenado)
    data_structs['mapa lobos']= None

###mapa con llave localización (latLong compuesto como se indica) y valor array de eventos con esa localización
    data_structs['mapa localizacion']=None

    data_structs['mapa nodos seguimiento']=None

    data_structs['lista nodos de encuentro']=lt.newList(datastructure='ARRAY_LIST')

    data_structs['grafo']=gr.newGraph()

    return(data_structs)
### FUNCIONES GENERALES QUE CREAN MAPA A PARTIR DE UN ARRAY
def crear_mapa_de_columna_a_partir_de_ARRAy(array, columna):

 
    mapa = mp.newMap(40, maptype='CHAINING' , loadfactor=0.5)
    
    ### Iteración para añadir
    i = 1
    tamanio_array = lt.size(array)
    while i<=tamanio_array:

        data = lt.getElement(array,i)

        add_data_y_o_casilla_al_mapa(mapa,data,columna)

        i+=1
    
    return mapa

    

    
def add_data_y_o_casilla_al_mapa(mapa, data,parametro):
 
    llave_casilla = data[parametro]
    

    exist_casilla = mp.contains(mapa,llave_casilla)
    if exist_casilla:
        entry = mp.get(mapa,llave_casilla)
        array_asociado = me.getValue(entry)
    else:
        array_asociado = new_casilla()
        mp.put(mapa,llave_casilla,array_asociado)
    
    lt.addLast(array_asociado,data)


def new_casilla():
    """
    Esta funcion crea la estructura de libros asociados
    a un año.
    """
   
    entry = lt.newList('ARRAY_LIST')
    return entry

# Funciones para agregar informacion al modelo

def add_data(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    lt.addLast(data_structs['lista total'],data)


# Funciones para creacion de datos

def new_data(id, info):
    """
    Crea una nueva estructura para modelar los datos
    """
    #TODO: Crear la función para estructurar los datos
    pass






#######                      CREAR GRAFO CON LAS ESPECIFICACIONES CORRESPONDIENTES



def crear_grafo(data_structs):

    ###a. Redondear
    redondear_lista_total(data_structs)
    poner_coordenada_en_formato_a_evento_Y_asociarlo_con_nodo_de_seguimiento(data_structs)

    ###b. mapa lobos
    crear_mapa_lobos(data_structs)

    ###C. mapa coordenadas

    crear
    return data_structs

###a. Redondear lista
def redondear_4_hacia_arriba(num):
    parte_decimal = str(num).split('.')[1]
    parte_entera =str(num).split('.')[0]
    cuatro_decimales = parte_decimal[0:4]
    num=float(parte_entera+'.'+cuatro_decimales)
    if num>0:
        num=num+0.0001
    return num

def redondear_lista_total(data_structs):
    lista_original = (data_structs['lista total'])

    size = lt.size(data_structs['lista total'])

    i =1

    while i<=size:
        evento = lt.getElement(lista_original,i)

        long = evento['location-long']
        lat = evento['location-lat']

        evento['location-long']=redondear_4_hacia_arriba(long)
        evento['location-lat']=redondear_4_hacia_arriba(lat)

        i+=1

    return data_structs


####b. mapa  por lobo, con arrays ordenados por tiempo y luego filtrados si 2 consecutivos tienen la misma localización

def crear_mapa_lobos(data_structs):
    mapa_lobos = crear_mapa_de_columna_a_partir_de_ARRAy(data_structs['lista total'],'individual-local-identifier')

    ###ordenar mapa
    llaves_mapa = lt.iterator(mp.keySet(mapa_lobos))

    for lobo in llaves_mapa:
        lista_eventos = devolver_value(mapa_lobos,lobo)
        quk.sort(lista_eventos,sort_criteria_tiempo)

    ### filtrar si hay repetido con lista auxiliar

    for lobo in llaves_mapa:
        lista_eventos = devolver_value(mapa_lobos,lobo)
        size =lt.size(lista_eventos)
        lista_aux = lt.newList('ARRAY_LIST')
        i=2
        ##añadir el primero
        primer_elemento =lt.getElement(lista_eventos,1)

        long = primer_elemento['location-long']
        lat = primer_elemento['location-lat']

        lt.addLast(lista_aux,primer_elemento)
        while i<=size:
            evento =lt.getElement(lista_eventos,i)

            if evento['location-long']!=long and evento['location-lat']!=lat:

                lt.addLast(lista_aux,evento)
                long=evento['location-long']
                lat=evento['location-lat']

            i+=1
        mp.remove(mapa_lobos,lobo)
        mp.put(mapa_lobos,lobo,lista_aux)

    data_structs['mapa lobos']=mapa_lobos


#### C. Hash coordenadas

def poner_coordenada_en_formato_a_evento_Y_asociarlo_con_nodo_de_seguimiento(data_structs):
    lista =data_structs['lista total']

    lista_iterable = lt.iterator(lista)

    for evento in lista_iterable:
        long=evento['location-long'].replace('.','p').replace('-','m')
        lat =evento['location lat'].replace('.','p').replace('-','m')
        id=evento['individual-local-identifier']

        coordenada_compuesta= long+'_'+lat
        evento['coordenada']=coordenada_compuesta

        nodo =coordenada_compuesta +'_'+id
        evento['nodo']=nodo
    return data_structs

def crear_mapa_coordenadas(data_structs):
    
    map= mp.newMap()

    lista_total = lt.iterator(data_structs['lista total'])


    for evento in lista_total:
        cor = evento['coordenada']
        estaa= mp.contains(map,cor)
        if estaa==False:
            lista = lt.newList()
            lt.addFirst(evento)
            mp.put(map, cor, lista)

        else:
            valor =devolver_value(map,cor)
            lt.addLast(valor,evento)

    


    data_structs['mapa localización']=map
    

    return data_structs


### iterar mapa lobos y añadir los nodos a un hash con valores None
def crear_nodos_de_seguimiento(data_structs):

    mapa_lobos =data_structs['mapa lobos']
    
    mapa_nodos_seguimiento =mp.newMap()

    lista_lobos =lt.iterator(mp.keySet(mapa_lobos))

    for lobo in lista_lobos:
        lista_eventos =lt.iterator(devolver_value(mapa_lobos,lobo))

        for evento in lista_eventos:
            nodo_asociado = evento['nodo']

            estaa=mp.contains(mapa_nodos_seguimiento,nodo_asociado)

            if estaa==False:
                mp.put(mapa_nodos_seguimiento,nodo_asociado,None)

    data_structs['mapa nodos de seguimiento']=mapa_nodos_seguimiento

    return data_structs


    










# Funciones de consulta
def devolver_value(map, key):
    llave_valor = mp.get(map, key)
    valor = me.getValue(llave_valor)
    
    return valor 
def get_data(data_structs, id):
    """
    Retorna un dato a partir de su ID
    """
    #TODO: Crear la función para obtener un dato de una lista
    pass


def data_size(data_structs):
    """
    Retorna el tamaño de la lista de datos
    """
    #TODO: Crear la función para obtener el tamaño de una lista
    pass


def req_1(data_structs):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
    pass


def req_2(data_structs):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    pass


def req_3(data_structs):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    pass


def req_4(data_structs):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    pass


def req_5(data_structs):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    pass


def req_6(data_structs):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    pass


def req_7(data_structs):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    pass


def req_8(data_structs):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    pass


# Funciones utilizadas para comparar elementos dentro de una lista

def compare(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    #TODO: Crear función comparadora de la lista
    pass

# Funciones de ordenamiento

def sort_criteria_tiempo(a,b):

        cod_1 = a["timestamp"].replace(':','').replace('-','').replace(' ','')
        cod_2 = b["timestamp"].replace(':','').replace('-','').replace(' ','')
        return(float(cod_1)<float(cod_2))

def sort_criteria(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    #TODO: Crear función comparadora para ordenar
    pass


def sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    pass
