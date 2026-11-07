
from lematizador_regex.lematizador_regex import tokenizadoregex, tokenizadoregextexto

#==================================================================
def construir_indice(tokens):
    indice = {}
    for palabra in tokens:
        if palabra not in indice:
            indice[palabra] = len(indice)
    return indice

#==================================================================
def construir_coocurrencia(tokens, indice, distancia):
    n = len(indice)
    matriz = [[0] * n for _ in range(n)]

    for i in range(len(tokens)):
        inicio = max(0, i - distancia)
        fin = min(len(tokens) - 1, i + distancia)

        for j in range(inicio, fin + 1):
            if i != j:
                fila = indice[tokens[i]]
                columna = indice[tokens[j]]
                matriz[fila][columna] += 1

    return matriz

#==================================================================
def print_coocurrencia(tokens, distancia):
    indice = construir_indice(tokens)
    vocabulario = [None] * len(indice)

    for palabra in indice:
        vocabulario[indice[palabra]] = palabra

    matriz = construir_coocurrencia(tokens, indice, distancia)

    print(vocabulario)

    for i in range(len(matriz)):
        print(vocabulario[i].ljust(12), matriz[i])

    return matriz, vocabulario, indice

#==================================================================
def buscar_palabra(matriz, vocabulario, palabra, indice):
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

    matriz, vocabulario, indice = print_coocurrencia(
        texto_original, distancia
    )

    return texto_original, texto_original, matriz, vocabulario, indice

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

        valor = buscar_palabra(matriz, vocabulario, palabra, indice)

        if valor is None:

            print("\nLa palabra no existe en el vocabulario.")

            respuesta = input("¿Desea agregarla? (s/n): ").lower()

            if respuesta == "s":
                texto, texto, matriz, vocabulario, indice = agregar_palabra(
                    texto, palabra_original, distancia
                )
                valor = buscar_palabra(matriz, vocabulario, palabra, indice)

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
