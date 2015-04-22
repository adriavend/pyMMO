__author__ = 'Adrian'

# Quita el ultimo caracter de una lista
def quitar_ultimo_caracter(lista):
    for i in range(len(lista)):
        lista[i] = lista[i][:-1]
    return lista

# Convierte una cadena en una lista
def listar_cadena(cadena):
    lista = []
    for i in range(len(cadena)):
        lista.append(cadena[i])
    return lista

def leer_mapa(archivo):
    # Abre y lee el archivo
    mapa = open(archivo, "r")
    # Lee todas las lineas del archivo. Tenemos una lista con todos las cadenas de caracteres por cada linea del archivo. por ej ["....M...", "..M..."]
    mapa = mapa.readlines()
    # Quitamos el ultimo caracter (salta de line \n)
    mapa = quitar_ultimo_caracter(mapa)

    for i in range(len(mapa)):
        #Convertimos cada cadena en una lista.
        mapa[i] = listar_cadena(mapa[i])

    # retornamos una lista con lista de caracteres.
    return mapa
