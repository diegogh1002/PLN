import re
import string
from lemas_excepciones import lemas_excepciones
import time
import tracemalloc

def tokenizador3(texto):
    tokens = []
    token = ""
    delimiters = string.whitespace
    tokens = re.findall(r"(?:\w|\d|[,/_@:\.-])+", texto)
    return tokens

def AMinusculas(texto):
    texto_nuevo = ""
    for letra in texto:
        if re.search(r"^[A-ZÁÉÍÓÚÑÜ]$", letra):
            letra = chr(ord(letra) + 32)
        texto_nuevo += letra
    return texto_nuevo

def ciclo_AMinusculas(texto):
    tokens = []
    for t in texto:
        tokens.append(AMinusculas(t))
    return tokens

def eliminador_stopwords(tokens):
    stop_words = r"\b(el|que|la|lo|los|las|de|del|en|a|un|uno|es|con|para|se|al)\b"
    tokens_nuevos = []

    for token in tokens:
        if not re.search(stop_words, token):
            tokens_nuevos.append(token)

    return tokens_nuevos

def aplicar_reglas(palabra):
    n = len(palabra)

    if re.search(r"iendo$", palabra) and n > 6:
        palabra = palabra[0:n-5] + "er"

    elif re.search(r"ando$", palabra) and n > 5:
        palabra = palabra[0:n-4] + "ar"

    elif re.search(r"ieron$", palabra) and n > 6:
        palabra = palabra[0:n-5] + "er"

    elif re.search(r"aron$", palabra) and n > 5:
        palabra = palabra[0:n-4] + "ar"

    elif re.search(r"emos$", palabra) and n > 5:
        palabra = palabra[0:n-4]

    elif re.search(r"ás$", palabra) and n > 4:
        palabra = palabra[0:n-2]

    elif re.search(r"án$", palabra) and n > 4:
        palabra = palabra[0:n-2]

    #elif re.search(r"es$", palabra) and n > 4:
        #palabra = palabra[0:n-2]

    elif re.search(r"s$", palabra) and n > 1:
        palabra = palabra[0:n]

    elif re.search(r"é$", palabra) and n > 4:
        palabra = palabra[0:n-1]

    elif re.search(r"á$", palabra) and n > 4:
        palabra = palabra[0:n-1]

    if re.search(r"^(\w|\d)", palabra) and re.search(r"(\.|,)$", palabra):
        palabra = re.search(
            r"(?:\w|\d|[/_@+,:\.-])+(?:\w|\d)|\w+", palabra
        ).group()

    return palabra

def lematizador_reglas_excepciones(palabra):
    if palabra in lemas_excepciones:
        return lemas_excepciones[palabra]
    else:
        return aplicar_reglas(palabra)

def lematizar(palabras):
    palabras_lematizadas = [None] * len(palabras)

    for i in range(len(palabras)):
        palabras_lematizadas[i] = lematizador_reglas_excepciones(palabras[i])

    return palabras_lematizadas

def procesar_texto(texto):
    tokens = tokenizador3(texto)
    tokens = ciclo_AMinusculas(tokens)
    tokens = lematizar(tokens)
    return tokens

def leer_texto(nombre_archivo):
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        texto = archivo.read()
    return texto

def construir_indice(tokens):
    indice = {}
    i = 0

    while i < len(tokens):
        if tokens[i] not in indice:
            indice[tokens[i]] = len(indice)
        i += 1

    return indice

def construir_coocurrencia(tokens, indice, distancia):
    n = len(indice)
    matriz = [[0 for j in range(n)] for i in range(n)]

    for i in range(len(tokens)):
        inicio = max(0, i - distancia)
        fin = min(len(tokens), i + distancia + 1)

        for j in range(inicio, fin):
            if i != j:
                fila = indice[tokens[i]]
                columna = indice[tokens[j]]
                matriz[fila][columna] += 1

    return matriz

def print_coocurrencia(tokens, distancia):
    indice = construir_indice(tokens)
    vocabulario = [None] * len(indice)

    for palabra in indice:
        vocabulario[indice[palabra]] = palabra

    matriz = construir_coocurrencia(tokens, indice, distancia)

    print("\nVocabulario:")
    print(vocabulario)

    print("\nMatriz de coocurrencia:")
    print("".ljust(15), end="")

    for palabra in vocabulario:
        print(palabra.ljust(12), end="")

    print()

    for i in range(len(matriz)):
        print(vocabulario[i].ljust(15), end="")

        for j in range(len(matriz[i])):
            print(str(matriz[i][j]).ljust(12), end="")

        print()

    return matriz, vocabulario, indice

def buscar_palabra(matriz, vocabulario, palabra, indice):
    if palabra in indice:
        posicion = indice[palabra]
        return matriz[posicion]

    return None

def agregar_palabra(texto_original, palabra_original, distancia):
    print("\n" + "-" * 50)
    print("              AGREGAR PALABRAS")
    print("-" * 50)

    print("\n¿Cómo deseas agregar la palabra?")
    print("1. Agregar únicamente la palabra.")
    print("2. Agregar palabras de contexto.")

    while True:
        opcion = input("\nSelecciona una opción: ")

        if opcion == "1" or opcion == "2":
            break

        print("Selecciona 1 o 2.")

    if opcion == "1" or distancia == 1:
        frase = palabra_original

    else:
        cantidad = distancia - 1

        while True:
            adicionales = input(
                f"\nIngresa las otras {cantidad} palabras: "
            )

            tokens_adicionales = procesar_texto(adicionales)

            if len(tokens_adicionales) == cantidad:
                break

            print(f"Debes ingresar exactamente {cantidad} palabras.")

        frase = palabra_original + " " + adicionales

    nuevos_tokens = procesar_texto(frase)

    print("\nFrase original agregada:")
    print(frase)

    print("\nFrase tokenizada y lematizada:")
    print(nuevos_tokens)

    texto_original += " " + frase

    tokens = procesar_texto(texto_original)

    print("\n" + "-" * 50)
    print("          MATRIZ ACTUALIZADA")
    print("-" * 50)

    matriz, vocabulario, indice = print_coocurrencia(
        tokens, distancia
    )

    return texto_original, tokens, matriz, vocabulario, indice

# PROGRAMA PRINCIPAL

archivos = ["textoprueba.txt"]

for archivo in archivos:
    texto_original = leer_texto(archivo)
    tokens = procesar_texto(texto_original)

    print("\n" + "-" * 50)
    print("          SISTEMA DE COOcurrencia")
    print("-" * 50)

    print("\nArchivo:", archivo)
    print("Total de palabras:", len(tokens))

    print("\n" + "-" * 50)

    while True:
        try:
            distancia = int(input("\nIngrese la distancia (1-5): "))

            if 1 <= distancia <= 5:
                break

            print("Ingrese un número entre 1 y 5.")

        except ValueError:
            print("Ingrese un número válido.")

    print("\nConstruyendo matriz de coocurrencia...")

    print("\n" + "-" * 50)
    print("              MATRIZ INICIAL")
    print("-" * 50)

    matriz, vocabulario, indice = print_coocurrencia(
        tokens, distancia
    )

    while True:
        print("\n" + "-" * 50)
        print("                 BÚSQUEDA")
        print("-" * 50)

        palabra_original = input("\nIngrese la palabra que desea buscar: ")

        tokens_busqueda = procesar_texto(palabra_original)

        if len(tokens_busqueda) != 1:
            print("\nDebe ingresar únicamente una palabra.")
            continue

        palabra = tokens_busqueda[0]

        print("\nPalabra lematizada:", palabra)

        resultado = buscar_palabra(
            matriz, vocabulario, palabra, indice
        )

        if resultado is not None:
            print("\nPalabras cercanas:")
            print("-" * 35)

            encontrada = False

            for i in range(len(resultado)):
                if resultado[i] > 0:
                    print(vocabulario[i], ":", resultado[i])
                    encontrada = True

            if not encontrada:
                print("No tiene palabras relacionadas.")

        else:
            print("\nLa palabra no existe en el vocabulario.")

            respuesta = input("¿Deseas agregarla? (s/n): ").lower()

            if respuesta == "s":
                texto_original, tokens, matriz, vocabulario, indice = agregar_palabra(
                    texto_original, palabra_original, distancia
                )

                resultado = buscar_palabra(
                    matriz, vocabulario, palabra, indice
                )

                if resultado is not None:
                    print("\nPalabras cercanas:")
                    print("-" * 35)

                    encontrada = False

                    for i in range(len(resultado)):
                        if resultado[i] > 0:
                            print(vocabulario[i], ":", resultado[i])
                            encontrada = True

                    if not encontrada:
                        print("No tiene palabras relacionadas.")

        continuar = input("\n¿Deseas buscar otra palabra? (s/n): ").lower()

        if continuar != "s":
            print("\n" + "-" * 50)
            print("             FIN DEL PROGRAMA")
            print("-" * 50)
            break