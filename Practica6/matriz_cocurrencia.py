from lematizador_regex.lematizador_regex import tokenizadoregex, tokenizadoregextexto
import numpy as np

#==================================================================
def construir_indice(tokens):
    indice = {}
    i = 0

    while i < len(tokens):
        palabra = tokens[i]
        if palabra not in indice:
            indice[palabra] = len(indice)
        i += 1

    return indice

#==================================================================
def construir_coocurrencia(tokens, distancia, vocabulario, indice):
    matriz = np.zeros((len(vocabulario), len(vocabulario)),dtype=np.int32)
    i = 0

    while i < len(tokens):
        inicio = max(0, i - distancia)
        fin = min(len(tokens) - 1, i + distancia)
        j = inicio

        while j <= fin:
            if i != j:
                fila = indice[tokens[i]]
                columna = indice[tokens[j]]
                matriz[fila, columna] += 1
            j += 1
        i += 1

    return matriz

#==================================================================
def print_coocurrencia(tokens, distancia):
    indice = construir_indice(tokens)
    vocabulario = [None] * len(indice)

    for palabra in indice:
        vocabulario[indice[palabra]] = palabra

    matriz = construir_coocurrencia(tokens, distancia, vocabulario, indice)

    print(vocabulario)

    print(matriz)

    return matriz, vocabulario, indice

#==================================================================
def buscar_palabra(matriz, palabra, indice):
    if palabra in indice:
        return matriz[indice[palabra]]
    return None

#==================================================================
def agregar_palabra(texto_original, palabra_original, distancia):

    opcion = input("\n1. Solo palabra\n2. Agregar contexto\nSeleccione: ")

    frase = palabra_original

    if opcion == "2" and distancia > 1:
        adicionales = input("Ingrese las palabras de contexto: ")
        frase += " " + adicionales

    nuevos_tokens = tokenizadoregextexto(frase)
    texto_original += nuevos_tokens

    print("\nFrase tokenizada y lematizada:")
    print(nuevos_tokens)

    matriz, vocabulario, indice = print_coocurrencia(texto_original, distancia) 

    return texto_original, matriz, vocabulario, indice

#==================================================================
# PROGRAMA PRINCIPAL
#==================================================================

archivos = ["textoprueba.txt"]

for archivo in archivos:

    texto = tokenizadoregex(archivo)

    print("\nARCHIVO:", archivo)

    distancia = int(input("\nIngrese la distancia de coocurrencia: "))

    matriz, vocabulario, indice = print_coocurrencia(texto, distancia)

    while True:

        palabra_original = input("\nIngrese la palabra: ")
        palabra = tokenizadoregextexto(palabra_original)[0]

        print("\nPalabra lematizada:", palabra)

        valor = buscar_palabra(matriz, palabra, indice)

        if valor is None:

            print("\nLa palabra no existe en el vocabulario.")

            respuesta = input("¿Desea agregarla? (s/n): ").lower()

            if respuesta == "s":
                texto, matriz, vocabulario, indice = agregar_palabra(texto, palabra_original, distancia)
                valor = buscar_palabra(matriz, palabra, indice)

        if valor is not None:
            print("\nPalabras cercanas:")

            encontradas = False

            for i in range(len(valor)):
                if valor[i] > 0:
                    print(vocabulario[i], ":", valor[i])
                    encontradas = True

            if not encontradas:
                print("No tiene palabras relacionadas.")

        continuar = input("\n¿Desea buscar otra palabra? (s/n): ").lower()

        if continuar != "s":
            break
