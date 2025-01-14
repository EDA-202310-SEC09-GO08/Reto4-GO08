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
import time
import csv
import sys
import tracemalloc
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp



"""
El controlador se encarga de mediar entre la vista y el modelo.
"""
csv.field_size_limit(2147483647)
default_limit = 1000
sys.setrecursionlimit(default_limit*100000)

def new_controller():
    """
    Crea una instancia del modelo
    """
    control = {
        "model": None
    }
    control["model"] = model.new_data_structs()
    
    return control


# Funciones para la carga de datos


def load_data(control, filename):
    """
    Carga los datos del reto
    """

    ###CArga datos
    file = cf.data_dir + filename
    input_file = csv.DictReader(open(file, encoding='utf-8'))
    catalog = control['model']
    for line in input_file:
        model.add_data(catalog, line)


##### Crea grafo
    model.crear_grafo(catalog)

    return control

def load_data_2(control,filename):
    file = cf.data_dir + filename
    input_file = csv.DictReader(open(file, encoding='utf-8'))
    catalog = control['model']
    for line in input_file:
        model.add_data_lobos(catalog, line)

    model.cargar_archivo_lobos(catalog)

    return control
# Funciones de ordenamiento

def sort(control):
    """
    Ordena los datos del modelo
    """
    #TODO: Llamar la función del modelo para ordenar los datos
    pass


# Funciones de consulta sobre el catálogo

def get_data(control, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Llamar la función del modelo para obtener un dato
    pass


def req_1(control, origen, destino):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    time1 = get_time()
    res = model.req_1(control["model"], origen, destino)
    time2 = get_time
    delta_t=delta_time(time1,time2)
    return res, delta_t


def req_2(control,nodo1, nodo2):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    time1=get_time()
    res = model.req_2(control,nodo1,nodo2)
    time2=get_time()
    delta_t=delta_time(time1,time2)
    return res, delta_t

def req_3(control):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    time1=get_time()
    res = model.req_3(control)
    time2=get_time()
    delta_t=delta_time(time1,time2)
    return res, delta_t


def req_4(control,lat1,long1,lat2,long2):
    """
    Retorna el resultado del requerimiento 4
    """
    time1=get_time()
    res = model.req_4(control['model'],lat1,long1,lat2,long2)
    time2=get_time()
    delta_t=delta_time(time1,time2)
    return res,delta_t


def req_5(control, nodo, distancia, min ):
    """
    Retorna el resultado del requerimiento 5
    """
    time1 = get_time()
    res = model.req_5(control["model"], min, nodo, distancia)
    time2 = get_time()
    delta_t=delta_time(time1,time2)
    return res, delta_t

def req_6(control, fecha_1, fecha_2, genero):
    """
    Retorna el resultado del requerimiento 6
    """
    time1 = get_time()
    res = model.req_6(control["model"], fecha_1, fecha_2, genero)
    time2 = get_time()
    delta_t=delta_time(time1,time2)
    return res, delta_t


def req_7(control,time1,time2,temp1,temp2):
    """
    Retorna el resultado del requerimiento 7
    """
    timea=get_time()
    res = model.req_7(control['model'],time1,time2,temp1,temp2)
    #print(len(res))
    time2=get_time()
    delta_t=delta_time(timea,time2)
    return res, delta_t


def req_8(control):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    pass


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed

def get_memory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def delta_memory(stop_memory, start_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory
