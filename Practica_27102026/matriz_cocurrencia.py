import re
import string
from lemas_excepciones import lemas_excepciones
import time
import tracemalloc

#==================================================================
def tokenizador3(texto):
    tokens = []
    token = ""

    delimiters = string.whitespace

    #if re.search(r"\W",texto[-1]):
        #texto = texto + '.'

    tokens = re.findall(r"(?:\w|\d|[,/_@:\.-])+", texto)
    #tokens = re.findall(r"(?:\w|\d)(?:\w|\d|[,/_@:\.-])+(?:\w|\d)|\w+", texto)

    return tokens

#==================================================================
def AMinusculas(texto):
    letras = ''

    for letra in texto:
        if re.search(r"^[A-ZÁÉÍÓÚÑÜ]", letra):
            letra = chr(ord(letra) + 32)

        letras += letra

    return letras

#==================================================================
def ciclo_AMinusculas(texto):

    textos_minusculas = []

    for t in texto:
        textos_minusculas += [AMinusculas(t)]

    texto = textos_minusculas

    return texto

#==================================================================
def eliminador_stopwords(tokens):

    tokens_nuevos = []
    for token in tokens:
        if not re.search(r"\b(el|que|la|lo|los|las|de|del|en|a|un|uno|es|con|para|se|al)\b", token):
            tokens_nuevos += [token]

    return tokens_nuevos

#==================================================================
def aplicar_reglas(palabra):
    n = len(palabra)

    if re.search(r"iendo$", palabra) and n > 6:
        return palabra[0:n-5] + "er"

    if re.search(r"ando$", palabra) and n > 5:
        return palabra[0:n-4] + "ar"

    if re.search(r"ieron$", palabra) and n > 6:
        return palabra[0:n-5] + "er"

    if re.search(r"aron$", palabra) and n > 5:
        return palabra[0:n-4] + "ar"

    if re.search(r"emos$", palabra) and n > 5:
        return palabra[0:n-4]

    if re.search(r"ás$", palabra) and n > 4:
        return palabra[0:n-2]

    if re.search(r"án$", palabra) and n > 4:
        return palabra[0:n-2]

    #if re.search(r"es$", palabra) and n > 3:
        #return palabra[0:n-2]

    if re.search(r"s$", palabra) and n > 1:
        return palabra[0:n]

    if re.search(r"é$", palabra) and n > 4:
        return palabra[0:n-1]

    if re.search(r"á$", palabra) and n > 4:
        return palabra[0:n-1]

    if re.search(r"^(\w|\d)", palabra) and re.search(r"(\.|,)$", palabra):
        palabra = re.search(r"(?:\w|\d|[/_@+,:\.-])+(?:\w|\d)|\w+", palabra).group()

    return palabra

#==================================================================
def lematizador_reglas_excepciones(palabra):
    if palabra in lemas_excepciones:
        return lemas_excepciones[palabra]

    else:
        return aplicar_reglas(palabra)

#==================================================================
def lematizar(palabras):
    texto_lematizado = [None] * len(palabras)

    for i in range(len(palabras)):
        palabra_lematizada = lematizador_reglas_excepciones(palabras[i])
        texto_lematizado[i] = palabra_lematizada

    return texto_lematizado

#==================================================================
def procesar_texto(texto):
    tokens = tokenizador3(texto)
    tokens = ciclo_AMinusculas(tokens)
    tokens = lematizar(tokens)

    return tokens

#==================================================================
def leer_texto(nombre_archivo):
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        texto = archivo.read()
    return texto

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
def construir_coocurrencia(tokens, indice, distancia):
    n = len(indice)

    matriz = [
        [0] * n
        for _ in range(n)
    ]

    i = 0

    while i < len(tokens):
        inicio = i - distancia

        if inicio < 0:
            inicio = 0

        fin = i + distancia

        if fin >= len(tokens):
            fin = len(tokens) - 1

        j = inicio

        while j <= fin:
            if i != j:
                fila = indice[tokens[i]]
                columna = indice[tokens[j]]
                matriz[fila][columna] += 1
            j += 1

        i += 1

    return matriz

#==================================================================
def print_coocurrencia(tokens, distancia):
    indice = construir_indice(tokens)

    vocabulario = [None] * len(indice)

    for palabra in indice:
        vocabulario[indice[palabra]] = palabra

    matriz = construir_coocurrencia(
        tokens,
        indice,
        distancia
    )

    print(vocabulario)

    i = 0

    while i < len(matriz):
        print(
            vocabulario[i].ljust(12),
            matriz[i]
        )
        i += 1

    return matriz, vocabulario, indice

#==================================================================
def buscar_palabra(matriz, vocabulario, palabra, indice):

    if palabra in indice:
        posicion = indice[palabra]
        return matriz[posicion]

    return None

#==================================================================
def agregar_palabra(texto_original, palabra_original, distancia):

    print("\n¿Cómo deseas agregar la palabra?")
    print("1. Agregar únicamente la palabra.")
    print("2. Agregar palabras de contexto.")

    while True:
        opcion = input("\nSeleccione una opción: ")

        if opcion == "1" or opcion == "2":
            break
        else:
            print("Opción inválida.")

    if opcion == "1" or distancia == 1:
        frase = palabra_original

    else:
        cantidad = distancia - 1

        while True:
            adicionales = input(
                "\nIngrese las otras " + str(cantidad) + " palabras: "
            )

            tokens_adicionales = procesar_texto(adicionales)

            if len(tokens_adicionales) == cantidad:
                break
            else:
                print("Debe ingresar exactamente", cantidad, "palabras.")

        frase = palabra_original + " " + adicionales

    nuevos_tokens = procesar_texto(frase)

    print("\nFrase tokenizada y lematizada:")
    print(nuevos_tokens)

    texto_original += " " + frase

    tokens = procesar_texto(texto_original)

    print("\n" + "-" * 90)
    print("MATRIZ DE COOcurrencia ACTUALIZADA")
    print("-" * 90)

    matriz, vocabulario, indice = print_coocurrencia(
        tokens,
        distancia
    )

    return texto_original, tokens, matriz, vocabulario, indice

#==================================================================
# PROGRAMA PRINCIPAL
#==================================================================

#archivos = ["texto01.txt", "texto02.txt", "texto03.txt"]
archivos = ["textoprueba.txt"]

print("\n")
print("=" * 90)
print("                 RESULTADOS DE DATOS")
print("=" * 90)

for archivo in archivos:

    texto_ = leer_texto(archivo)

    texto = procesar_texto(texto)

    print("\n")
    print("-" * 90)
    print("ARCHIVO:", archivo)
    print("-" * 90)

    while True:
        try:
            distancia = int(input("\nIngrese la distancia de coocurrencia: "))

            if 1 <= distancia <= 5:
                matriz, vocabulario, indice = print_coocurrencia(texto,distancia)
                
                while True:
                    palabra_original = input("\nIngrese la palabra: ")
                    tokens_busqueda = procesar_texto(palabra_original)
                    if len(tokens_busqueda) != 1:
                        print("Ingrese únicamente una palabra.")
                        continue

                    palabra = tokens_busqueda[0]
                    print("\nPalabra lematizada:", palabra)
                    valor = buscar_palabra(matriz,vocabulario,palabra,indice)
                    if valor is not None:
                        print("\nPalabras cercanas:")
                        encontrada = False

                        for i in range(len(valor)):
                            if valor[i] > 0:
                                print(vocabulario[i], ":", valor[i])
                                encontrada = True

                        if not encontrada:
                            print("No tiene palabras relacionadas.")
                            
                    else:
                        print("\nLa palabra no existe en el vocabulario.")
                        respuesta = input("¿Desea agregarla? (s/n): ").lower()

                        if respuesta == "s":
                            texto_original, texto, matriz, vocabulario, indice = agregar_palabra(texto_original,palabra_original,distancia)

                            valor = buscar_palabra(matriz,vocabulario,palabra,indice)

                            if valor is not None:
                                print("\nPalabras cercanas:")
                                encontrada = False

                                for i in range(len(valor)):
                                    if valor[i] > 0:
                                        print(vocabulario[i], ":", valor[i])
                                        encontrada = True

                                if not encontrada:
                                    print("No tiene palabras relacionadas.")

                    continuar = input("\n¿Desea buscar otra palabra? (s/n): ").lower()

                    if continuar != "s":
                        break
                break
            else:
                print("Por favor, ingrese un número entre 1 y 5.")

        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número entero.")