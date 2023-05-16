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
import math 
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
##mapa cuya llave es el indicador del nodo(coordenada) y el valor una lista de nodos de seguimiento asociados a dicho nodo
    data_structs['mapa nodos de encuentro']=None
    data_structs['grafo']=gr.newGraph(directed=True)
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

    crear_mapa_coordenadas(data_structs)

    #####D. mapa nodos de seguimiento

    crear_nodos_de_seguimiento(data_structs)

    ###E. Crear nodos de encuentro
    crear_nodos_de_encuentro(data_structs)

    ####F. Poner nodos  en grafo
    poner_nodos__en_grafo(data_structs)

    ###G. Crear arcos entre nodos de seguimiento
    crear_arcos_nodos_seguimiento(data_structs)

    ####H. Crear arcos para los nodos de encuentro
    poner_arcos_encuentro(data_structs)
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

        long = float(evento['location-long'])
        lat = float(evento['location-lat'])

        evento['location-long']=round(long,4)
        evento['location-lat']=round(lat,4)

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
        long=str(evento['location-long']).replace('.','p').replace('-','m')
        lat =str(evento['location-lat']).replace('.','p').replace('-','m')
        id=str(evento['individual-local-identifier'])

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
            lt.addFirst(lista,evento)
            mp.put(map, cor, lista)

        else:
            valor =devolver_value(map,cor)
            lt.addLast(valor,evento)

    


    data_structs['mapa localizacion']=map
    

    return data_structs


### iterar mapa lobos y añadir los nodos a un hash con valor localización asociada
def crear_nodos_de_seguimiento(data_structs):

    mapa_lobos =data_structs['mapa lobos']
    
    mapa_nodos_seguimiento =mp.newMap()

    lista_lobos =lt.iterator(mp.keySet(mapa_lobos))

    for lobo in lista_lobos:
        lista_eventos =lt.iterator(devolver_value(mapa_lobos,lobo))

        for evento in lista_eventos:
            nodo_asociado = evento['nodo']
            localizacion_asociada=evento['coordenada']

            estaa=mp.contains(mapa_nodos_seguimiento,nodo_asociado)

            if estaa==False:
                mp.put(mapa_nodos_seguimiento,nodo_asociado,localizacion_asociada)

    data_structs['mapa nodos de seguimiento']=mapa_nodos_seguimiento

    return data_structs

### mapa con llave el nodo de encuentro y el valor los nodos de seguimiento asociados(en array)
def crear_nodos_de_encuentro(data_structs):

    mapa_nodos_encuentro = mp.newMap()
    mapaeventos_en_coordendad= data_structs['mapa localizacion']

    lista_coordenadas=mp.keySet(mapaeventos_en_coordendad)
    #voy por toda las locations
    for coordenada in lt.iterator(lista_coordenadas):
        lista_eventos=devolver_value(mapaeventos_en_coordendad,coordenada)
        #print(lista_eventos)
        #encuentro nodos asociados y los pongo en  mapa auxiliar (por el momento)
        mapa_auxiliar=mp.newMap()
        for evento in lt.iterator(lista_eventos):
            nodo_asociado =evento['nodo']
            #reviso si esta y si no la agrego al mapa auxiliar
            estaa=mp.contains(mapa_auxiliar,nodo_asociado)
            if estaa == False:
                mp.put(mapa_auxiliar, nodo_asociado,None)
                
        #si el mapa tiene un tamaño diferente a 1, es nodo encuentro, se ponne en el mapa y se le da por valor lista llaves de mapa auxiliar
        lista_auxiliar=mp.keySet(mapa_auxiliar)
        size_mapa_auxiliar =lt.size(lista_auxiliar)

        if size_mapa_auxiliar != 1:
            mp.put(mapa_nodos_encuentro,coordenada,lista_auxiliar)
    data_structs['mapa nodos de encuentro']=mapa_nodos_encuentro
    return data_structs



####F Poner nodos de encuentro y seguimiento en el grafo

def poner_nodos__en_grafo(data_structs):
    grafo = data_structs['grafo']
    lista_nodos_1=mp.keySet(data_structs['mapa nodos de seguimiento'])
    lista_nodos_2=mp.keySet(data_structs['mapa nodos de encuentro'])

    for nodo in lt.iterator(lista_nodos_1):
        gr.insertVertex(grafo,nodo)

    for nodo in lt.iterator(lista_nodos_2):
        gr.insertVertex(grafo,nodo)

    return data_structs

###g. crear arcos seguimiento
def funcion_distancias_lat_long(latitud1,longitud1,latitud2,longitud2):
    r = 6371
    c = math.pi/180
    d =r*2*math.asin(math.sqrt(math.sin(c*(latitud1-latitud2)/2)**2 + math.cos(c*latitud1) * math.cos(c*latitud2)*math.sin(c*(longitud1-longitud2)/2)**2))

    return d
def crear_arcos_nodos_seguimiento(data_structs):
    mapa_lobos= data_structs['mapa lobos']
    lista_lobos =mp.keySet(mapa_lobos)
    grafo =data_structs['grafo']

    for lobo in lt.iterator(lista_lobos):
        
        array_eventos=devolver_value(mapa_lobos,lobo)
        size =lt.size(array_eventos)

        i=1
        while i<size:
            evento_1 =lt.getElement(array_eventos,i)
            evento_2=lt.getElement(array_eventos,i+1)
            ###nodos
            nodo_1=evento_1['nodo']
            nodo_2=evento_2['nodo']
            ### lat,long 1
            lat_1=evento_1['location-lat']
            long_1=evento_1['location-long']
            ###lat long 2
            lat_2=evento_2['location-lat']
            long_2=evento_2['location-long']

            distancia=funcion_distancias_lat_long(lat_1,long_1,lat_2,long_2) 

            gr.addEdge(grafo,nodo_1,nodo_2,distancia) 
            i+=1

    return data_structs  

###H. Arcos nodos de encuentro
def poner_arcos_encuentro(data_structs):
    grafo=data_structs['grafo']
    mapa_nodos_encuentro=data_structs['mapa nodos de encuentro']
    lista_nodos_encuentro = mp.keySet(mapa_nodos_encuentro)

    for nodo_encuentro in lt.iterator(lista_nodos_encuentro):
        lista_nodos_asociados=devolver_value(mapa_nodos_encuentro,nodo_encuentro)

        for nodo_asociado in lt.iterator(lista_nodos_asociados):
            gr.addEdge(grafo,nodo_asociado,nodo_encuentro)
            gr.addEdge(grafo,nodo_encuentro,nodo_asociado)
            

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


def req_4(data_structs,lat_1,long_1,lat_2,long_2):
    """
    Función que soluciona el requerimiento 4
    """
    grafo=data_structs['grafo']
    nodo_dist_inicio=encontrar_nodo_encuentro_mas_cercano(data_structs,lat_1,long_1)
    nodo_inicio=nodo_dist_inicio[0]
    distancia_entre_punto_inicio_nodo=nodo_dist_inicio[1]
    ###

    nodo_dist_fin=encontrar_nodo_encuentro_mas_cercano(data_structs,lat_2,long_2)
    nodo_fin=nodo_dist_fin[0]
    distancia_entre_punto_fin_nodo=nodo_dist_fin[1] 

    pass



def encontrar_nodo_encuentro_mas_cercano(data_structs,lat,long):

    mapa_encuentro=data_structs['mapa nodos de encuentro']
    
    lista_encuentro =mp.keySet(mapa_encuentro)
    lista_encuentro_it =lt.iterator(mp.keySet(mapa_encuentro))

    encuentro_mas_cerca=lt.getElement(lista_encuentro,1)
    distancia_menor=9999999999999
    for nodo in lista_encuentro_it:
        coordenada = nodo.replace('m','-').replace('p','.').split('_')
        lat_nodo=float(coordenada[0])
        long_nodo=float(coordenada[1])

        distancia_a_punto= funcion_distancias_lat_long(lat,long,lat_nodo,long_nodo)

        if distancia_a_punto<distancia_menor:
            encuentro_mas_cerca=nodo
            distancia_menor=distancia_a_punto


    return nodo,distancia_menor


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
