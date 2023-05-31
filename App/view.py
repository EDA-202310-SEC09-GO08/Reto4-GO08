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
import threading
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
import folium
"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def devolver_value(map, key):
    llave_valor = mp.get(map, key)
    valor = me.getValue(llave_valor)
    
    return valor 
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
            
            size = 'BA-Grey-Wolf-tracks-utf8-5pct.csv'
            lobos='BA-Grey-Wolf-individuals-utf8-5pct.csv'
            return size,lobos
        elif int(porcentaje) == 3:
            size = 'BA-Grey-Wolf-tracks-utf8-10pct.csv'
            lobos='BA-Grey-Wolf-individuals-utf8-10pct.csv'
            return size,lobos
        elif int(porcentaje) == 4:
            size = 'BA-Grey-Wolf-tracks-utf8-20pct.csv'
            lobos='BA-Grey-Wolf-individuals-utf8-20pct.csv'
            return size,lobos
        elif int(porcentaje) == 5:
            size = 'BA-Grey-Wolf-tracks-utf8-30pct.csv'
            lobos='BA-Grey-Wolf-individuals-utf8-30pct.csv'
            return size,lobos
        elif int(porcentaje) == 6:
            size = 'BA-Grey-Wolf-tracks-utf8-50pct.csv'
            lobos='BA-Grey-Wolf-individuals-utf8-50pct.csv'
            return size,lobos
            
        elif int(porcentaje) == 1:
            size = 'BA-Grey-Wolf-tracks-utf8-small.csv'
            lobos='BA-Grey-Wolf-individuals-utf8-small.csv'
            return size,lobos
        elif int(porcentaje) == 7:
            size = 'BA-Grey-Wolf-tracks-utf8-80pct.csv'
            lobos='BA-Grey-Wolf-individuals-utf8-80pct.csv'
            return size,lobos
        elif int(porcentaje) == 8:
            size = 'BA-Grey-Wolf-tracks-utf8-large.csv'
            lobos='BA-Grey-Wolf-individuals-utf8-large.csv'
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




#### FUNCIONES ASOCIADAS A IMPRIMIR LA CARGA DE DATOS

def calc_eventos_filt_hay(control):
    ds=control['model']
    mapa =ds['mapa lobos']
    lobos =lt.iterator(mp.keySet(mapa))
    j=0
    for lobo in lobos:
        size =lt.size(model.devolver_value(mapa,lobo))

        j+=size

    return j

def dic_representa_nodo_encuentro(nodo_encuentro,data_structs):

    form_corr=nodo_encuentro.replace('p','.').replace('m','-')
    lat_long=form_corr.split('_')

    dic_nodo_enc={}
    long = lat_long[0]
    lat=lat_long[1]

    array_nodos_seg = devolver_value(data_structs['mapa nodos de encuentro'],nodo_encuentro)

    array_it=lt.iterator(array_nodos_seg)

    string_lobos=''
    lobos_asociados=0
    for nodo in array_it:
        nodo_split=nodo.split('_')
        lobo=nodo_split[2]+'_'+nodo_split[3]
        string_lobos+=lobo+', '
        lobos_asociados+=1
    dic_nodo_enc['node id']=nodo_encuentro
    dic_nodo_enc['lat']=lat
    dic_nodo_enc['long']=long
    dic_nodo_enc['wolfs']=string_lobos
    dic_nodo_enc['n wolfs']=lobos_asociados

    return dic_nodo_enc

def lista_10_dics_a_imprimir(data_structs):

    mapa_nodos_encuentro=data_structs['mapa nodos de encuentro']
    lista_nodos=mp.keySet(mapa_nodos_encuentro)
    size=lt.size(lista_nodos)

    lista_10_nodos=[]
    lista_10_nodos.append(lt.getElement(lista_nodos,1))
    lista_10_nodos.append(lt.getElement(lista_nodos,2))
    lista_10_nodos.append(lt.getElement(lista_nodos,3))
    lista_10_nodos.append(lt.getElement(lista_nodos,4))
    lista_10_nodos.append(lt.getElement(lista_nodos,5))


    lista_10_nodos.append(lt.getElement(lista_nodos,size-1))
    lista_10_nodos.append(lt.getElement(lista_nodos,size-2))
    lista_10_nodos.append(lt.getElement(lista_nodos,size-3))
    lista_10_nodos.append(lt.getElement(lista_nodos,size-4))
    lista_10_nodos.append(lt.getElement(lista_nodos,size-5))    
#
    i=0
    lista_10_dics=[]
    while i<10:
        dic=dic_representa_nodo_encuentro(lista_10_nodos[i],data_structs) 
        lista_10_dics.append(dic)
        i+=1

    return lista_10_dics

def print_carga_datos(control):
    dos_archivos = menu_archivo()
    archivo_tracks=dos_archivos[0]
    archivo_lobos=dos_archivos[1]

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



    ### EDGE FEATURES

    print('---------EDGES FEATURES------------ ')
    print('')
    print('')

    n_edges=gr.numEdges(data_structs['grafo'])

    n_track= data_structs['n arcos de seguimiento']
    n_gathering=n_edges-n_track
    print('Number of gathering edges: '+str(n_gathering))
    print('Number of tracking edges '+str(n_track))
    print('Total edges: '+str(n_edges))

    print('---------GRAPH AREA------------ ')
    print('')
    print('')

    print('Min-max latitude: '+str(data_structs['menor lat'])+' and '+str(data_structs['mayor lat']))
    print('Min-max long: '+str(data_structs['menor long'])+' and '+str(data_structs['mayor long']))


    print('First 5 and last 5 gathering nodes loaded: ')
    lista_filtrada=lista_10_dics_a_imprimir(data_structs)
    tabulate_respuesta = tabulate(lista_filtrada, headers='keys', maxcolwidths =[30]*4, maxheadercolwidths=[30]*4)
    print(tabulate_respuesta)
    pass


def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    origen = input("Ingrese el identificador del punto de origen: ")
    destino = input( "Ingrese el identificador del punto de destino: ")
    respuesta = controller.req_1(control, origen, destino)
    
    pass
#Long-111.874754_Lat57.498278
#Long-111.921908_Lat56.56768

def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    print()
    # TODO: Imprimir el resultado del requerimiento 2
    nodo1 = "m111p862_57p449"
    nodo2 = "m111p908_57p427"
    #nodo1=(input('Nodo 1: '))
    #nodo2=(input('Nodo 2: '))
    res = controller.req_2(control, nodo1, nodo2)
    print(tabulate(res[0][0], headers="keys", tablefmt= "grid", maxcolwidths=40, maxheadercolwidths=40 ))
    lat_c= (control['model']['mayor lat']   + control['model']['menor lat'] )/2
    long_c=(control['model']['mayor long']   + control['model']['menor long'] )/2

    mapa=folium.Map(location=[lat_c,long_c],zoom_start=5)
    i = 1
    for indv in lt.iterator(res[0][1]):
        if i + 1 < lt.size(res[0][1]):
            indv2 = lt.getElement(res[0][1], i+1)
            punto = indv.replace('m','-').replace('p','.').split('_')
            lat = float(punto[1])
            lon = float(punto[0])
            folium.Marker(location=[lat,lon],icon=folium.Icon(color='darkblue',icon='fire')).add_to(mapa)
            punto2 = indv2.replace('m','-').replace('p','.').split('_')
            lat2 = float(punto2[1])
            lon2 = float(punto2[0])
            folium.Marker(location=[lat2,lon2],icon=folium.Icon(color='darkblue',icon='fire')).add_to(mapa)
            locs=[(lat,lon),(lat2,lon2)]
            folium.PolyLine(locs,color='pink',weight=5,opacity=0.8).add_to(mapa)
        i +=1
    mapa.save("C:/Users/olgay/Downloads/mapa.html")

    print( " El tiempo es de:" + str(res[1]))
        



def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    res = controller.req_3(control)
    print("There are " + str(res[0][0]) + " strongly connectec components (SCC) in the graph ")
    print( "The top 5 SCC in the graph are: ")
    print(tabulate(res[0][1], headers="keys", tablefmt= "grid", maxcolwidths=40, maxheadercolwidths=40 ))
    lat_c= (control['model']['mayor lat']   + control['model']['menor lat'] )/2
    long_c=(control['model']['mayor long']   + control['model']['menor long'] )/2
    colores = ["darkblue", "pink", "red", "green", "black"]
    mapa=folium.Map(location=[lat_c,long_c],zoom_start=5)
    llaves = res[0][3]
    col = 0
    for cada in lt.iterator(llaves):
        i = 1
        esta = devolver_value(res[0][2], cada)
        for indv in lt.iterator(esta):
            if i + 1 < lt.size(esta):
                indv2 = lt.getElement(esta, i+1)
                punto = indv.replace('m','-').replace('p','.').split('_')
                lat = float(punto[1])
                lon = float(punto[0])
                folium.Marker(location=[lat,lon],icon=folium.Icon(color=colores[col],icon='fire')).add_to(mapa)
                punto2 = indv2.replace('m','-').replace('p','.').split('_')
                lat2 = float(punto2[1])
                lon2 = float(punto2[0])
                folium.Marker(location=[lat2,lon2],icon=folium.Icon(color=colores[col],icon='fire')).add_to(mapa)
                locs=[(lat,lon),(lat2,lon2)]
                folium.PolyLine(locs,color='pink',weight=5,opacity=0.8).add_to(mapa)
            i +=1
        col +=1
    mapa.save("C:/Users/olgay/Downloads/mapa.html")

    print( " El tiempo es de:" + str(res[1]))

def devolver_value(map, key):
    llave_valor = mp.get(map, key)
    valor = me.getValue(llave_valor)
    
    return valor
def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    lat1=float(input('Latitud inicial: '))
    long1=float(input('Longitud inicial: '))
    lat2=float(input('Latitud final: '))
    long2=float(input('Longitud final: '))
    #plong1=-111.911
    #plat1=57.431
    #plong2=-111.865
    #plat2=57.453
    res=controller.req_4(control,lat1,long1,lat2,long2)
    time=res[1]
    res=res[0]

    print(' La distancia entre el punto GPS de origen y el punto de encuentro más cercano: ')
    print(str(res[0])+' km')
    print('')

    print(' La distancia el punto de encuentro de destino más cercano y el punto GPS de destino: ')
    print(str(res[1])+' km')
    print('')
    if len(res)==4:
        print('Nodo inicio: '+res[2])
        print('Nodo fin: '+res[3])
        print('No hay camino')
        print('tiempo: '+str(time))
        return None
    print('  La distancia total que tomará el recorrido entre los puntos de encuentro de origen y destino: ')
    print(str(res[2])+'km')
    print('')
    print('Total de nodos:')
    print(res[3])
    print('')  
    print('Total de arcos:')
    print(res[4])
    print('')  
    print('Total de lobos distintos que UTILIZAN el camino:')
    print(res[8])
    print('')  
    print(' Los tres primeros puntos de la ruta en orden ascendente son :')
    tabulete5=tabulate(res[5], headers='keys', maxcolwidths =[30]*6, maxheadercolwidths=[30]*6)
    print(tabulete5)
    print('')
    print(' Los tres últimos puntos de la ruta en orden descendente son :')
    tabulete6=tabulate(res[6], headers='keys', maxcolwidths =[30]*6, maxheadercolwidths=[30]*6)
    print(tabulete6)
    print('') 
    lat_c= (control['model']['mayor lat']   + control['model']['menor lat'] )/2
    long_c=(control['model']['mayor long']   + control['model']['menor long'] )/2

    mapa=folium.Map(location=[lat_c,long_c],zoom_start=5)
    folium.Marker(location=[lat1,long1],icon=folium.Icon(color='darkblue',icon='fire')).add_to(mapa)
    folium.Marker(location=[lat2,long2],icon=folium.Icon(color='red',icon='fire')).add_to(mapa)
    for dic in res[5]:
            folium.Marker(location=[dic['lat'],dic['long']],icon=folium.Icon(color='green',icon='fire')).add_to(mapa)

    for dic in res[6]:
        folium.Marker(location=[dic['lat'],dic['long']],icon=folium.Icon(color='orange',icon='fire')).add_to(mapa)
    
    for arco in lt.iterator(res[7]):
        vertexA=arco['vertexA'].replace('m','-').replace('p','.').split('_')
        vertexB=arco['vertexB'].replace('m','-').replace('p','.').split('_')
        latA=float(vertexA[1])
        latB=float(vertexB[1])
        longA=float(vertexA[0])
        longB=float(vertexB[0])
        locs=[(latA,longA),(latB,longB)]
        folium.PolyLine(locs,color='black',weight=5,opacity=0.8).add_to(mapa)
    mapa.save("C:/Users/samis/Downloads/mapa.html")
    
    print('tiempo: '+str(time))


#
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
    fecha1='2012-11-28 00:00'
    fecha2='2014-05-17 23:59'
    temp1='-17.3'
    temp2='9.7'
    print('LOading correspondig graph:')

    
    res=controller.req_7(control,fecha1,fecha2,temp1,temp2)
    a=res[0][3]
    print('Graph featrures:')
    print('Total nodes: '+str(gr.numVertices(res[0][3]['grafo'])))
    print('Total edges: '+str(gr.numEdges(res[0][3]['grafo'])))
    print("Considering the folowwing date range: ")
    print("Start date : " + str(fecha1))
    print("End date : " +str(fecha2))
    print("Considering the folowwing temperature range: ")
    print("low temperature: " + str(temp1))
    print("Hight temperature: " +str(temp2))
    print("There are " + str(res[0][0]) + " strongly connectec components (SCC) in the graph ")
    print( "The first 3 and the last 3 SCC in the graph are: ")
    print(tabulate(res[0][1], headers="keys", tablefmt= "grid", maxcolwidths=40, maxheadercolwidths=40 ))
    print("The longest path per sccid: ")
    print(tabulate(res[0][2], headers="keys", tablefmt= "grid", maxcolwidths=40, maxheadercolwidths=40 ))

    print( " El tiempo es de:" + str(res[1]))
    # TODO: Imprimir el resultado del requerimiento 7
    


def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass


# Se crea el controlador asociado a la vista


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
                control = new_controller()
                print_carga_datos(control)

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


