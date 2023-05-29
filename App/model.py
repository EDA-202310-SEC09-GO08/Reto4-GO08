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
from tabulate import tabulate
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

    data_structs['lista archivo lobos']=lt.newList(datastructure='ARRAY_LIST')

    data_structs['grafo no dirigido']=gr.newGraph(directed=False)
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

def add_data_lobos(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    lt.addLast(data_structs['lista archivo lobos'],data)

####CARGAR ARCHIVO DE LOBOS

def cargar_archivo_lobos(data_strucst):
    lista_lobos =data_strucst['lista archivo lobos']
    anadir_individual_id_a_lobo(data_strucst)
    data_strucst['mapa archivo lobos']=crear_mapa_de_columna_a_partir_de_ARRAy(lista_lobos,'individual-id')

    return data_strucst

# Funciones para creacion de datos


def anadir_individual_id_a_lobo(data_structs):

    lista_lobos = lt.iterator(data_structs['lista archivo lobos'])

    for lobo in lista_lobos:
        animal_id =lobo['animal-id']
        tag_id=lobo['tag-id']
        individual_id=animal_id+'_'+tag_id
        lobo['individual-id']=individual_id

    return data_structs





#######                      CREAR GRAFO CON LAS ESPECIFICACIONES CORRESPONDIENTES



def crear_grafo(data_structs):

    ###a. Redondear:
    ### recoje lista total y redondea las coordenadas a 3 decimales
    redondear_lista_total(data_structs)
    ### Añade a cada evento su coordenada asociada y su nodo de seguimiento asociado 
    poner_coordenada_en_formato_a_evento_Y_asociarlo_con_nodo_de_seguimiento(data_structs)

    ###b. mapa lobos
    ## Crea mapa con llave animal-id y valor array ordenado por fecha de los eventos asociados a ese lobo
    crear_mapa_lobos(data_structs)
    ##de cada array un elemento si el anterior tiene su misma coordenada.
    filtrar_mapa_lobos(data_structs)

    ###C. mapa coordenadas
    ## mediante iteración del mapa lobos, crea mapa con llave coordenada y valor array eventos en dicha coordenada
    crear_mapa_coordenadas(data_structs)

    #####D. mapa nodos de seguimiento
    ## Iterando mapa lobos, crea mapa de nodos de seguimiento cuyo valor es la coordenada.
    crear_nodos_de_seguimiento(data_structs)

    ###E. Crear nodos de encuentro
    ### Iterando mapa de coordenadas, crea mapa con llave nodo-id y valor array de nodos de seguimiento adyacentes.
    crear_nodos_de_encuentro(data_structs)

    ####F. Poner nodos  en grafo
    ##Itera los mapas y pone los nodos en el grafo
    poner_nodos__en_grafo(data_structs)

    ###G. Crear arcos entre nodos de seguimiento

    ## Itera mapa lobos para crear arcos de nodos de seguimiento
    crear_arcos_nodos_seguimiento(data_structs)

    ####H. Crear arcos para los nodos de encuentro
    ###Itera mapa nodos de encuentro para poner arcos adyacentes.
    poner_arcos_encuentro(data_structs)


    ##I. rectangulo de area requerido para view
    anadir_menor_mayor_lat_log(data_structs)
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

        evento['location-long']=round(long,3)
        evento['location-lat']=round(lat,3)

        i+=1

    return data_structs


####b. mapa  por lobo, con arrays ordenados por tiempo y luego filtrados si 2 consecutivos tienen la misma localización

def crear_mapa_lobos(data_structs):
    mapa_lobos = crear_mapa_de_columna_a_partir_de_ARRAy(data_structs['lista total'],'individual-id')

    ###ordenar mapa
    llaves_mapa = lt.iterator(mp.keySet(mapa_lobos))

    for lobo in llaves_mapa:
        #print('h')
        lista_eventos = devolver_value(mapa_lobos,lobo)

        quk.sort(lista_eventos,sort_criteria_tiempo)


    data_structs['mapa lobos']=mapa_lobos
    return data_structs

def filtrar_mapa_lobos(data_structs):
    mapa_lobos = data_structs['mapa lobos']


    ###ordenar mapa
    llaves_mapa = lt.iterator(mp.keySet(mapa_lobos))
    for lobo_1 in llaves_mapa:
        #print('kj')
        lista_eventos = devolver_value(mapa_lobos,lobo_1)
        size =lt.size(lista_eventos)
        lista_aux = lt.newList('ARRAY_LIST')
        i=2
        ##añadir el primero
        primer_elemento =lt.getElement(lista_eventos,1)

        long = primer_elemento['location-long']
        lat = primer_elemento['location-lat']
        coordenada=primer_elemento['coordenada']

        lt.addLast(lista_aux,primer_elemento)
        while i<=size:
            evento =lt.getElement(lista_eventos,i)

            if evento['coordenada']!=coordenada:

                lt.addLast(lista_aux,evento)
            long=evento['location-long']
            lat=evento['location-lat']
            coordenada=evento['coordenada']

            i+=1

        #print(lt.size(lista_aux)-lt.size(lista_eventos))
        #print('hola')
    
        
        mp.remove(mapa_lobos,lobo_1)
        mp.put(mapa_lobos,lobo_1,lista_aux)


    data_structs['mapa lobos']=mapa_lobos

    return data_structs

#### C. Hash coordenadas

def poner_coordenada_en_formato_a_evento_Y_asociarlo_con_nodo_de_seguimiento(data_structs):
    lista =data_structs['lista total']

    lista_iterable = lt.iterator(lista)

    for evento in lista_iterable:
        animal_id=evento['individual-local-identifier']
        tag_id =evento['tag-local-identifier']
        individual_id=animal_id+'_'+tag_id

        long=str(evento['location-long']).replace('.','p').replace('-','m')
        lat =str(evento['location-lat']).replace('.','p').replace('-','m')
       

        coordenada_compuesta= long+'_'+lat
        evento['coordenada']=coordenada_compuesta

        nodo =coordenada_compuesta +'_'+individual_id
        evento['nodo']=nodo
        evento['individual-id']=individual_id
    return data_structs

#def crear_mapa_coordenadas(data_structs):
    
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

def crear_mapa_coordenadas(data_structs):
    
    map= mp.newMap()

    mapa_lobos=data_structs['mapa lobos']
    lobos = lt.iterator(mp.keySet(mapa_lobos))

    for lobo in lobos:
        lista=lt.iterator(devolver_value(mapa_lobos,lobo))
        for evento in lista:
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
    grafo_NO_dirigido=data_structs['grafo no dirigido']
    lista_nodos_1=mp.keySet(data_structs['mapa nodos de seguimiento'])
    lista_nodos_2=mp.keySet(data_structs['mapa nodos de encuentro'])

    for nodo in lt.iterator(lista_nodos_1):
        gr.insertVertex(grafo,nodo)
        gr.insertVertex(grafo_NO_dirigido,nodo)

    for nodo in lt.iterator(lista_nodos_2):
        gr.insertVertex(grafo,nodo)
        gr.insertVertex(grafo_NO_dirigido,nodo)


    return data_structs

###g. crear arcos seguimiento
def funcion_distancias_lat_long(latitud1,longitud1,latitud2,longitud2):
    r = 6371
    c = math.pi/180
    d =r*2*math.asin(math.sqrt(math.sin(c*(latitud1-latitud2)/2)**2 + math.cos(c*latitud1) * math.cos(c*latitud2)*math.sin(c*(longitud1-longitud2)/2)**2))

    return d
def crear_arcos_nodos_seguimiento(data_structs,positivos=True):
    mapa_lobos= data_structs['mapa lobos']
    lista_lobos =mp.keySet(mapa_lobos)
    grafo =data_structs['grafo']
    grafo_NO_dirigido=data_structs['grafo no dirigido']
    j=0
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
            if positivos==True:
                gr.addEdge(grafo,nodo_1,nodo_2,distancia) 
            else:
                gr.addEdge(grafo,nodo_1,nodo_2,-distancia) 
            gr.addEdge(grafo_NO_dirigido,nodo_1,nodo_2,distancia) 
            i+=1
            j+=1

    data_structs['n arcos de seguimiento']=j

    return data_structs  

###H. Arcos nodos de encuentro
def poner_arcos_encuentro(data_structs):
    grafo=data_structs['grafo']
    grafo_NO_dirigido=data_structs['grafo no dirigido']
    mapa_nodos_encuentro=data_structs['mapa nodos de encuentro']
    lista_nodos_encuentro = mp.keySet(mapa_nodos_encuentro)

    for nodo_encuentro in lt.iterator(lista_nodos_encuentro):
        lista_nodos_asociados=devolver_value(mapa_nodos_encuentro,nodo_encuentro)

        for nodo_asociado in lt.iterator(lista_nodos_asociados):
            gr.addEdge(grafo,nodo_asociado,nodo_encuentro)
            gr.addEdge(grafo,nodo_encuentro,nodo_asociado)
            gr.addEdge(grafo_NO_dirigido,nodo_encuentro,nodo_asociado)

    return data_structs


#### I. Encontrar mayor y menor por coordenadas

def encontrar_menor(lista, criterio):
    
    i =0
    tamanio = lt.size(lista)
    
    menor = 9999999999999
    while i <= tamanio:
        exacto = lt.getElement(lista,i)
        if float(exacto[criterio])<float(menor):
            
            menor = exacto[criterio]
        i+=1
    return menor

def encontrar_mayor(lista, criterio):
    
    i =0
    tamanio = lt.size(lista)
    
    mayor=-999999999999
    while i <= tamanio:
        exacto = lt.getElement(lista,i)
        if float(exacto[criterio])>float(mayor):
            
            mayor = exacto[criterio]
        i+=1
    return mayor

def anadir_menor_mayor_lat_log(data_structs):
    ## lat
    data_structs['menor lat']=encontrar_menor(data_structs['lista total'],'location-lat')
    data_structs['mayor lat']=encontrar_mayor(data_structs['lista total'],'location-lat')

### Long
    data_structs['menor long']=encontrar_menor(data_structs['lista total'],'location-long')
    data_structs['mayor long']=encontrar_mayor(data_structs['lista total'],'location-long')

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


def req_2(data_structs, nodo1, nodo2):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    busqueda = dfs.DepthFirstSearch(data_structs["model"]["grafo"], nodo1)
    hay = dfs.hasPathTo(busqueda,nodo2)
    if hay == True:
        como = dfs.pathTo(busqueda,nodo2)
    lista = []

    i = 1 
    lista = lt.newList()
    while i <= 5:
        pos = lt.getElement(como,i)
        lt.addLast(lista, pos)
        i +=1

    a = 5
    while a > 0:
        size = lt.size(como) - a 
        pos = lt.getElement(como, size)
        lt.addLast(lista,pos)
        a +=1
    
    res = []
    vez = 0
    for valor in lt.iterator(lista):
        dic = {}
        cada_una = separar(valor)
        dic["Location long-aprox"] = cada_una[0]
        dic["location lat-aprox"] = cada_una[1]
        dic["node-id"] = valor
        cuantos = devolver_value(data_structs["model"]["mapa nodos de encuentro"], valor)
        size = lt.size(cuantos)
        adelante = adelante(como, vez)
        dic["individual-id"]
        dic["individual-count"] = size
        dic["edge-to"] = adelante
        if adelante != "unknown":
            dist = gr.getEdge(data_structs["model"]["grafo"], valor, adelante)
        else:
            dist = "unknown"
            
        dic["edge distance- km"] = dist
        vez +=1
    res.append(dic)
    return res 
    
def individual( lista):
    res = []
    for ind in lt.iterator(lista):
        res.append(ind)
    return res 
def adelante(lista, pos):
    if pos < 4:
        donde = lt.getElement(lt.size(lista)- pos)
    elif pos == 4 and pos < 9:
        donde = lt.getElement(lista,pos-3)
    else:
        donde = "unknown "
    return donde

def req_3(data_structs):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    grafo=data_structs["model"]['grafo']
    kosaraju = scc.KosarajuSCC(grafo)
    "los puntos conectados "
    total = scc.connectedComponents(kosaraju)
    keys = mp.keySet(kosaraju["idscc"])
    mapa = mp.newMap()

    for manada in lt.iterator(keys):
        "invertir las llaves como valores dentro de una lista y el valor se volvio la llave"
        actual = devolver_value(kosaraju["idscc"],manada)
        esta = mp.contains(mapa, actual)
        if esta == False:
            lista = lt.newList()
            lt.addFirst(lista,manada)
            mp.put(mapa,actual,lista)
        else:
            agregar = devolver_value(mapa, actual)
            lt.addLast(agregar, manada)


    llaves_scc = mp.keySet(mapa)
    i = 1 
    final = lt.newList()
    'encontrar el top 5 '
    while i <= 5:
        mayor = 0 
        sccc = 0
        a = 1
        
        while a <= lt.size(llaves_scc):
            sccdid = lt.getElement(llaves_scc,a)
            cantidad_list = devolver_value(mapa,sccdid)
            if lt.size(cantidad_list) > mayor:
                mayor = lt.size(cantidad_list)
                sccc = sccdid
                pos = a 
            a += 1
        lt.addLast(final,sccc)  
        lt.deleteElement(llaves_scc, pos)
        i +=1

    ' ir poniendo requerimiento por requerimiento'
    valor = pedido(data_structs["model"],mapa,final)

    return total, valor

def pedido( data_structs, mapa, lista_mejores):
    valor = []
    for ultima in lt.iterator(lista_mejores):
        respuesta = {}
        respuesta["SCCID"] = ultima 
        respuesta["NODEIDS"] = node_ids(mapa,ultima)
        lista = devolver_value(mapa,ultima)
        respuesta["SCC Size "] = lt.size(lista)
        max_mins = encontrar(lista, data_structs["mapa archivo lobos"])
        respuesta ["min-lat"] = max_mins[0]
        respuesta ["max-lat"] = max_mins[1]
        respuesta ["min-lon"] = max_mins[2]
        respuesta ["max-lon"] = max_mins[3]
        respuesta["wolf Count"] = max_mins[4]
        respuesta["Wolf details"] = max_mins[5]
        valor.append(respuesta)
    return valor 

def separar(el_str):

    lista = el_str.replace("m", "-").replace("p",".")
    separado = lista.split("_")
    return separado

def encontrar (lista,mapa_lobos ):
    menorlat = 999999999999
    menorlon = 9999999999999

    mayorlat= -999999999999
    mayorlon = -9999999999999
    cantidad = []
    lobos = 0 
    for codigo in lt.iterator(lista):
        separado = separar(codigo)
        "encontrar los mayores y menores"
        if float(separado[1]) > mayorlat:
            mayorlat = float(separado[1])
        if float(separado[1]) < menorlat:
            menorlat = float(separado[1])
        if float(separado[0]) > mayorlon:
            mayorlon = float(separado[0])
        if float(separado[0]) < menorlon:
            menorlon = float(separado[0])
        if len(separado)== 4:
            id = separado[2] + "_" + separado[3]
            esta = False 
            'verificar cuantos lobos hay en la manada'
            if len(cantidad) == 0:
                cantidad.append(id)
                lobos +=1
            for ids in cantidad:
                if ids == id:
                    esta = True
            if esta == False:
                lobos +=1 
                cantidad.append(id)
    lobos_info = []
    a = 0
    while a < 3 and a < len(cantidad):
        identificador = cantidad[a]
        lobos_info.append(caracteristicas(mapa_lobos, identificador))
        a +=1
    size = len(cantidad)
    if size >= 6:
        i = 3
        while i > 0 :
            identificador = cantidad[size - i ]
            lobos_info.append(caracteristicas(mapa_lobos, identificador))
            i-=1
    final_lobos = tabulate(lobos_info, headers="keys", tablefmt= "grid", maxcolwidths=5, maxheadercolwidths=5  )
        
    res = [menorlat, mayorlat, menorlon, mayorlon, lobos, final_lobos]
    return res 
def caracteristicas (lobo, id):
    ' sacarle las caracteristicas al lobo'
    res = {}
    x = devolver_value(lobo, id)
    info = x["elements"][0]
    res["individual-id"] = id
    if info["animal-sex"] != "":
        res["animal-sex"] = info["animal-sex"]
    else:
        res["animal-sex"] = "Unknown"
    
    if info["animal-life-stage"] != "":
        res["animal-life-stage"] = info["animal-life-stage"]
    else:
        res["animal-life-stage"] = "Unknown"

    if info["study-site"] != "":
        res["study-site"] = info["study-site"]
    else:
        res["study-site"] = "Unknown"
    
    if info["deployment-comments"] != "":
        res["deployment-comments"] = info["deployment-comments"]
    else:
        res["deployment-comments"] = "Unknown"
    return res 
    
def node_ids (mapa, llave):
    ' sacar los primero tres y los ultimos tres ids segun la lista'
    valor = devolver_value(mapa,llave)
    i = 1
    respuesta = []
    if lt.size(valor) >= 3:
        while i <= 3:
            pos = lt.getElement(valor,i)
            respuesta.append(pos)
            i += 1
        a = 3
        size = lt.size(valor)
        while a > 0:
            posicion = size - a
            respuesta.append(lt.getElement(valor,posicion ))
            a -=1 
    else:
        pos =lt.getElement(valor,1)
        respuesta.append(pos)
    return respuesta


def req_4(data_structs,lat_1,long_1,lat_2,long_2):
    """
    Función que soluciona el requerimiento 4
    """
    grafo=data_structs['grafo']

    ### retorna encuentro más cerca y distancia a este
    nodo_dist_inicio=encontrar_nodo_encuentro_mas_cercano(data_structs,lat_1,long_1)
    nodo_inicio=nodo_dist_inicio[0]
    distancia_entre_punto_inicio_nodo=nodo_dist_inicio[1]
    ###

    nodo_dist_fin=encontrar_nodo_encuentro_mas_cercano(data_structs,lat_2,long_2)
    nodo_fin=nodo_dist_fin[0]
    distancia_entre_punto_fin_nodo=nodo_dist_fin[1] 

    ###recorridos minimos del nodo de incio a todos los demás
    recorridos_inicio=bf.BellmanFord(grafo,nodo_inicio)

    recorrido_min=bf.pathToArray(recorridos_inicio,nodo_fin)

    

    #print(nodo_inicio)
    #print(nodo_fin)
    
    total_arcos=lt.size(recorrido_min)
    total_nodos=total_arcos+1
    
    #print(total_arcos)
    it=lt.iterator(recorrido_min)
    dist_total=0
    for i in it:
        #print(i)
        dist_total+=i['weight']

    #print(dist_total)
    print(recorrido_min)
    prim=tres_primeros_nodos(recorrido_min,data_structs['mapa nodos de encuentro'])
    ult=tres_ultimos_nodos(recorrido_min,data_structs['mapa nodos de encuentro'])
    lista_a_devolver=[]
    lista_a_devolver.append(distancia_entre_punto_inicio_nodo)
    lista_a_devolver.append(distancia_entre_punto_fin_nodo)
    lista_a_devolver.append(dist_total)
    lista_a_devolver.append(total_nodos)
    lista_a_devolver.append(total_arcos)
    lista_a_devolver.append(prim)
    lista_a_devolver.append(ult)
    lista_a_devolver.append(recorrido_min)

    return lista_a_devolver
    pass



def encontrar_nodo_encuentro_mas_cercano(data_structs,lat,long):

    mapa_encuentro=data_structs['mapa nodos de encuentro']
    
    lista_encuentro =mp.keySet(mapa_encuentro)
    lista_encuentro_it =lt.iterator(mp.keySet(mapa_encuentro))

    encuentro_mas_cerca=None
    distancia_menor=9999999999999
    for nodo in lista_encuentro_it:
        coordenada = nodo.replace('m','-').replace('p','.').split('_')
        lat_nodo=float(coordenada[1])
        long_nodo=float(coordenada[0])

        distancia_a_punto= funcion_distancias_lat_long(lat,long,lat_nodo,long_nodo)

        if distancia_a_punto<distancia_menor:
            encuentro_mas_cerca=nodo
            distancia_menor=distancia_a_punto


    return encuentro_mas_cerca,distancia_menor
def tres_primeros_nodos(recorrido_min,mapa_nodos_encuentro):
    lista_dics=[]
    size=lt.size(recorrido_min)
    i=0
    while i<3:
        datos={}
        arco=lt.getElement(recorrido_min,size-i)
        id_punto=arco['vertexA']
        form_corr=id_punto.replace('p','.').replace('m','-')
        long_lat=form_corr.split('_')
        long=long_lat[0]
        lat=long_lat[1]
        if len(long_lat)==2:
            array_nodos_seguimiento=devolver_value(mapa_nodos_encuentro,id_punto)
            n_lobos=lt.size(array_nodos_seguimiento)
            it =lt.iterator(array_nodos_seguimiento)
            lobos=''
            for nodo in it:

                compuesto=nodo.split('_')
                lobo=compuesto[2]+'_'+compuesto[3]
                lobos+=lobo+', '

        else:


            lobos=long_lat[2]+'_'+long_lat[3]
            n_lobos=1

        datos['id_nodo']=id_punto
        datos['long']=long
        datos['lat']=lat
        datos['lobos']=lobos
        datos['n_lobos']=n_lobos
        datos['distancia']=arco['weight']
        lista_dics.append(datos)
        #print(datos)
        i+=1
    
    return lista_dics

    
def tres_ultimos_nodos(recorrido_min,mapa_nodos_encuentro):
    lista_dics=[]
    size=lt.size(recorrido_min)
    i=1
    while i<=3:
        datos={}
        arco=lt.getElement(recorrido_min,i)
        id_punto=arco['vertexB']
        form_corr=id_punto.replace('p','.').replace('m','-')
        long_lat=form_corr.split('_')
        long=long_lat[0]
        lat=long_lat[1]
        if len(long_lat)==2:
            array_nodos_seguimiento=devolver_value(mapa_nodos_encuentro,id_punto)
            n_lobos=lt.size(array_nodos_seguimiento)
            it =lt.iterator(array_nodos_seguimiento)
            lobos=''
            for nodo in it:

                compuesto=nodo.split('_')
                lobo=compuesto[2]+'_'+compuesto[3]
                lobos+=lobo+', '

        else:


            lobos=long_lat[2]+'_'+long_lat[3]
            n_lobos=1

        datos['id_nodo']=id_punto
        datos['long']=long
        datos['lat']=lat
        datos['lobos']=lobos
        datos['n_lobos']=n_lobos
        datos['distancia']=arco['weight']
        lista_dics.append(datos)
        #print(datos)
        i+=1
    
    return lista_dics

def identifica_n_lobos_en_camino(camino):
    it=lt.iterator(camino)
    

def req_5(data_structs):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    pass

##### Funciones para 6 y 7 de filtrar array_ordenado de eventos por rango de fechas y temperaturas, devuelven el arrray 
### ordenadp por tiempo con los eventos dentro del rango
def array_ordenado_filtrado_por_rango_fechas(array,fecha1,fecha2):
    ### Devuelve un array filtrado ordenado de los eventos en ese rango
    fecha_in=float(fecha1.replace(':','').replace('-','').replace(' ',''))
    fecha_fin=float(fecha2.replace(':','').replace('-','').replace(' ',''))
    array_filt=lt.newList(datastructure='ARRAY_LIST')
    size=lt.size(array)

    i=1
    while i<=size:
        evento= lt.getElement(array,i)
        fecha=float(evento["timestamp"].replace(':','').replace('-','').replace(' ',''))
        if fecha >=fecha_in and fecha<=fecha_fin:
            lt.addLast(array_filt,evento)

        if fecha>fecha_fin:
            break

        i+=1
    
    return array_filt

## Filtra array por rango de temperatura
def filtrar_array_por_temp(array,temp1,temp2):
    temp_in=float(temp1)
    temp_fin=float(temp2)
    array_filt=lt.newList(datastructure='ARRAY_LIST')
    size=lt.size(array)

    i=1
    while i<=size:
        evento= lt.getElement(array,i)
        temp=float(evento["external-temperature"])
        if temp >=temp_in and temp <=temp_fin:
            lt.addLast(array_filt,evento)
        i+=1
    return array_filt

def filtrar_mapa_lobos_porintervalos(data_structs,time1,time2,temp1,temp2):
    mapa_lobos=data_structs['mapa lobos']
    mapa_filt=mp.newMap()
    lobos=lt.iterator(mp.keySet(mapa_lobos))
    
    for lobo in lobos:
        array_0=devolver_value(mapa_lobos,lobo)
        arrayfilt=array_ordenado_filtrado_por_rango_fechas(array_0,time1,time2)
        arrayfilt=filtrar_array_por_temp(arrayfilt,temp1,temp2)
        mp.put(mapa_filt,lobo,arrayfilt)

    data_structs['mapa lobos']=mapa_filt

    return data_structs

##### filtra el data structs según los parámetros para req 7
        
def crear_grafo_filtrado(data_structs,time1,time2,temp1,temp2):

    ##a. mapa filt
    filtrar_mapa_lobos_porintervalos(data_structs,time1,time2,temp1,temp2)

    ###C. mapa coordenadas

    data_structs['mapa localizacion']=None

    crear_mapa_coordenadas(data_structs)

    #####D. mapa nodos de seguimiento
    data_structs['mapa nodos de seguimiento']=None

    crear_nodos_de_seguimiento(data_structs)

    ###E. Crear nodos de encuentro
    data_structs['mapa nodos de encuentro']=None
    crear_nodos_de_encuentro(data_structs)

    ####F. Poner nodos  en grafo
    data_structs['grafo']=gr.newGraph(directed=True)
    
    poner_nodos__en_grafo(data_structs)

    ###G. Crear arcos entre nodos de seguimiento
    crear_arcos_nodos_seguimiento(data_structs,False)

    ####H. Crear arcos para los nodos de encuentro
    poner_arcos_encuentro(data_structs)

    print(gr.numEdges(data_structs['grafo']))
    print(gr.numVertices(data_structs['grafo']))
    print(mp.size(data_structs['mapa nodos de seguimiento']))
    print(mp.size(data_structs['mapa nodos de encuentro']))


def req_6(data_structs):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    pass


def req_7(data_structs,time1,time2,temp1,temp2):
    """
    Función que soluciona el requerimiento 7
    """
    crear_grafo_filtrado(data_structs,time1,time2,temp1,temp2)
    grafo=data_structs['grafo']
    kosaraju = scc.KosarajuSCC(grafo)
    "los puntos conectados "
    total = scc.connectedComponents(kosaraju)
    keys = mp.keySet(kosaraju["idscc"])
    mapa = mp.newMap()

    for manada in lt.iterator(keys):
        "invertir las llaves como valores dentro de una lista y el valor se volvio la llave"
        actual = devolver_value(kosaraju["idscc"],manada)
        esta = mp.contains(mapa, actual)
        if esta == False:
            lista = lt.newList()
            lt.addFirst(lista,manada)
            mp.put(mapa,actual,lista)
        else:
            agregar = devolver_value(mapa, actual)
            lt.addLast(agregar, manada)


    llaves_scc = mp.keySet(mapa)
    i = 1 
    final = lt.newList()
    'encontrar el top 3 '
    while i <= 3:
        mayor = 0 
        sccc = 0
        a = 1
        
        while a <= lt.size(llaves_scc):
            sccdid = lt.getElement(llaves_scc,a)
            cantidad_list = devolver_value(mapa,sccdid)
            if lt.size(cantidad_list) > mayor:
                mayor = lt.size(cantidad_list)
                sccc = sccdid
                pos = a 
            a += 1
        lt.addLast(final,sccc)  
        lt.deleteElement(llaves_scc, pos)
        i +=1
    e = 1
    while e <= 3:
        mayor = 99999999999
        sccc = 0
        a = 1
        
        while a <= lt.size(llaves_scc):
            sccdid = lt.getElement(llaves_scc,a)
            cantidad_list = devolver_value(mapa,sccdid)
            if lt.size(cantidad_list) < mayor:
                mayor = lt.size(cantidad_list)
                sccc = sccdid
                pos = a 
            a += 1
        lt.addLast(final,sccc)  
        lt.deleteElement(llaves_scc, pos)
        e +=1

    respuesta = pedido(data_structs, mapa, final)

    return total, respuesta
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
