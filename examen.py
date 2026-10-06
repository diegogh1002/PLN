import string

from lemas_excepciones import lemas_excepciones
# ### medir consumo de memoria y tiempo
import time
import tracemalloc
import numpy as np
from sklearn.decomposition import PCA

#####################################################################################
####    Tokenizador de palabras
def tokenizador3(texto):

    tokens = []
    token = ""

    delimiters = string.whitespace + string.punctuation + string.digits

    if texto[-1] != ' ' and texto[-1] != '.' and texto[-1] != '\n' and texto[-1] != '\r' and texto[-1] != '\t':
        texto = texto + '.'


    for i in range(0, len(texto)):

        if (texto[i] == ' ' or texto[i] == '.'):
            if token != "":
                tokens += [token]
                token = ""
        else:
            if texto[i] not in delimiters:
                token = token + texto[i]

    return tokens


#####################################################################################
####    Convertidor de Mayusculas a minusculas
###     Silla - silla

def AMinusculas(texto):
    letras = ''
    for letra in texto:
        # A-Z
        if ord(letra) >= 65 and ord(letra) <= 90:
            letra = chr(ord(letra) + 32)
        # Á É Í Ó Ú
        elif ord(letra) in [193, 201, 205, 211, 218]:
          letra = chr(ord(letra) + 32)
        letras += letra
    return letras

#####################################################################################
####    Eliminador de Stop Words

def eliminador_stopwords(tokens):

    stop_words = ["el", "que", "la", "lo", "los", "las",
                  "de", "del", "en", "a", "un", "uno",
                  "es", "con", "para", "se", "al"]
    tokens_nuevos = []
    for token in tokens:
        if token not in stop_words:
            tokens_nuevos += [token]
    return tokens_nuevos


#####################################################################################
####    Lematizador de palabras

def aplicar_reglas(palabra):
    ## Verbos terminando en en "ando"
    n = len(palabra)
    if palabra[n-5:n] == "ando" and n > 5:
        return palabra[0:n-5] + "ar"
    ## Verbos terminando en "iendo"
    if palabra[n-6:n] == "iendo" and n > 6:
        return palabra[0:n-6] + "er"
    ## Verbos terminando en "es"
    if palabra[n-2:n] == "es" and n > 3:
        return palabra[0:n-2]
    ## Verbos terminando en "s"
    if palabra[n-1:n] == "s" and n > 1:
        return palabra[0:n-1]

    # AGREGAR: pasado
    if palabra[n-4:n] == "aron" and n > 5:
        return palabra[0:n-4] + "ar"

    if palabra[n-5:n] == "ieron" and n > 6:
        return palabra[0:n-5] + "er"

    # AGREGAR: futuro
    if palabra[n-1:n] == "é" and n > 4:
        return palabra[0:n-1]

    if palabra[n-2:n] == "ás" and n > 4:
        return palabra[0:n-2]

    if palabra[n-1:n] == "á" and n > 4:
        return palabra[0:n-1]

    if palabra[n-4:n] == "emos" and n > 5:
        return palabra[0:n-4]

    if palabra[n-2:n] == "án" and n > 4:
        return palabra[0:n-2]

    return palabra


#Comprobar si estamos en las excepciones o estamos en las reglas
def lematizador_reglas_excepciones(palabra):
    if palabra in lemas_excepciones:
        return lemas_excepciones[palabra]
    else:
        return aplicar_reglas(palabra)


#Lematizar
def lematizar(palabras):
    #palabras = tokenizador3(texto)
    texto_lematizado = [None]*len(palabras)
    for i in range(len(palabras)):
        palabra_lematizada = lematizador_reglas_excepciones(palabras[i])
        #print (palabra_lematizada)
        texto_lematizado[i] = palabra_lematizada
    return texto_lematizado


#for documentos in corpus:
    #print(lematizador(documentos))


#####################################################################################
####    Leer texto de un archivo
def leer_texto(nombre_archivo):

    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        texto = archivo.read()
    return texto

#####################################################################################
####    CODIFICACION ONE HOT ENCODING
def codificacion_one_hot(tokens):
    tokens_unicos = []
    for token in tokens:
        if token not in tokens_unicos:
            tokens_unicos += [token]

    vectores = {}
    for token in tokens_unicos:
        vector = [0] * len(tokens_unicos)
        indice = tokens_unicos.index(token)
        vector[indice] = 1
        vectores[token] = vector
    return vectores

def generar_matriz_one_hot(vocabulario_general):

    vectores = codificacion_one_hot(vocabulario_general)
    palabras = list(vectores.keys())
    matriz = np.array([vectores[p] for p in palabras])
    print("Dimensiones de la matriz One Hot:", matriz.shape)
    return palabras, matriz


def verificar_one_hot(matriz):

    solo_binarios = bool(np.all((matriz == 0) | (matriz == 1)))
    unos_por_fila = np.sum(matriz == 1, axis=1)
    todos_un_uno = bool(np.all(unos_por_fila == 1))
    print("Solo contiene 0 y 1:", solo_binarios)
    print("Cada fila tiene exactamente un 1:", todos_un_uno)
    print("Mínimo / máximo de unos por fila:", unos_por_fila.min(), "/", unos_por_fila.max())
    return solo_binarios and todos_un_uno


def aplicar_pca(matriz, n_componentes=2):

    pca = PCA(n_components=n_componentes)
    reducida = pca.fit_transform(matriz)
    var = pca.explained_variance_ratio_
    acumulada = np.cumsum(var)

    print("Dimensión original:", matriz.shape)
    print("Dimensión reducida:", reducida.shape)
    for i in range(n_componentes):
        print(f"Componente {i+1}: varianza explicada = {var[i]:.6f} ({var[i]*100:.3f}%)"
              f" | acumulada = {acumulada[i]:.6f} ({acumulada[i]*100:.3f}%)")
    return reducida, pca


def distancia_euclidiana(a, b):
    return float(np.sqrt(np.sum((a - b) ** 2)))


def comparar_palabras(palabra1, palabra2, palabras, matriz, reducida):

    i = palabras.index(palabra1)
    j = palabras.index(palabra2)

    print(f"--- {palabra1} ---")
    print("One Hot (posición del 1:", i, "):", matriz[i])
    print("2 componentes:", reducida[i])
    print(f"--- {palabra2} ---")
    print("One Hot (posición del 1:", j, "):", matriz[j])
    print("2 componentes:", reducida[j])

    d_antes = distancia_euclidiana(matriz[i], matriz[j])
    d_despues = distancia_euclidiana(reducida[i], reducida[j])
    print(f"\nDistancia euclidiana antes de PCA:   {d_antes:.6f}")
    print(f"Distancia euclidiana después de PCA: {d_despues:.6f}")
    return d_antes, d_despues


def conclusion(pca, d_antes, d_despues):

    retenida = float(np.sum(pca.explained_variance_ratio_))
    perdida = 1 - retenida
    print(f"\nVarianza conservada con 2 componentes: {retenida*100:.3f}%")
    print(f"Varianza perdida: {perdida*100:.3f}%")
    print(f"La distancia pasó de {d_antes:.4f} a {d_despues:.4f}.")
    if perdida > 1e-6:
        print("Se pierde información: la distancia original entre palabras distintas "
              "no se conserva y la mayor parte de la varianza queda fuera de los 2 componentes.")
    else:
        print("Se conserva prácticamente toda la información.")



def ejercicio_3(vocabulario_general, palabra1, palabra2):
    palabras, matriz = generar_matriz_one_hot(vocabulario_general)
    print()
    verificar_one_hot(matriz)
    print()
    reducida, pca = aplicar_pca(matriz, 2)
    print()
    d_antes, d_despues = comparar_palabras(palabra1, palabra2, palabras, matriz, reducida)
    conclusion(pca, d_antes, d_despues)
    return palabras, matriz, reducida, pca



#####################################################################################
####    Main

#texto = "..VOy a la rÉpRob4#$#$#546ar / % . el  S6#%#5í.  6  88808 no .... Es#%#53t678uDio PLN...979"

archivos = ["documentoa.txt", "documentob.txt", "documentoc.txt"]
#archivos = ["/content/documentoa.txt", "/content/documentob.txt", "/content/documentoc.txt"]

for archivo in archivos:

    tracemalloc.start()
    t_ini = time.time()
    texto = leer_texto(archivo)

    print("\n" )
    print("\n" )
    print("\n" )
    print("\n" + "=" * 90)
    print("PROCESANDO:", archivo)
    print("=" * 90)
    #print("Original: ", texto)

    texto = AMinusculas(texto)
    texto = tokenizador3(texto)

    print("Número de tokens (palabras antes de eliminar stop words): ", len(texto))

    texto = eliminador_stopwords(texto)

    print("Número de tokens (palabras después de eliminar stop words): ", len(texto))

    #t_fin = time.time()
    #actual, pico = tracemalloc.get_traced_memory()
    #print("El tiempo de ejecución fue de:", t_fin - t_ini, "segundos")
    #print("La memoria pico fue de:", pico / 10**3, "Kb")
    #print("La memoria actual es de:", actual / 10**3, "Kb")
    #print("Tokenizado: ", texto)

    texto = lematizar(texto)

    print("Número de tokens (palabras después de lematizar): ", len(texto))

    print("Primeros 15 tokens del resultado final ", texto[:15])


    t_fin = time.time()
    actual, pico = tracemalloc.get_traced_memory()

    print("El tiempo de ejecución fue de:", t_fin - t_ini, "segundos")
    print("La memoria pico fue de:", pico / 10**3, "Kb")
    print("La memoria actual es de:", actual / 10**3, "Kb")
    #print("Tokenizado y lematizado: ", texto)

    tracemalloc.stop()

    #####################################################################################
    ####    AGREGADO: Guardar los documentos procesados

    if archivo == archivos[0]:
        texto_A = texto[:]

    elif archivo == archivos[1]:
        texto_B = texto[:]

    elif archivo == archivos[2]:
        texto_C = texto[:]


#####################################################################################
####    PUNTO 2: VOCABULARIOS

# Vocabulario A

vocabulario_A = []

for palabra in texto_A:

    if palabra not in vocabulario_A:
        vocabulario_A += [palabra]


# Vocabulario B

vocabulario_B = []

for palabra in texto_B:

    if palabra not in vocabulario_B:
        vocabulario_B += [palabra]


# Vocabulario C

vocabulario_C = []

for palabra in texto_C:

    if palabra not in vocabulario_C:
        vocabulario_C += [palabra]


#####################################################################################
####    Vocabulario general

vocabulario_general = []

for palabra in vocabulario_A:

    if palabra not in vocabulario_general:
        vocabulario_general += [palabra]

for palabra in vocabulario_B:

    if palabra not in vocabulario_general:
        vocabulario_general += [palabra]

for palabra in vocabulario_C:

    if palabra not in vocabulario_general:
        vocabulario_general += [palabra]


#####################################################################################
####    Tamaño de los vocabularios

print("\n")
print("=" * 90)
print("PUNTO 2: TAMAÑO DE LOS VOCABULARIOS")

print("Tamaño del vocabulario A:", len(vocabulario_A))
print("Tamaño del vocabulario B:", len(vocabulario_B))
print("Tamaño del vocabulario C:", len(vocabulario_C))
print("Tamaño del vocabulario general:", len(vocabulario_general))


#####################################################################################
####    Palabras compartidas

compartidas_AB = []

for palabra in vocabulario_A:

    if palabra in vocabulario_B:
        compartidas_AB += [palabra]


compartidas_AC = []

for palabra in vocabulario_A:

    if palabra in vocabulario_C:
        compartidas_AC += [palabra]


compartidas_BC = []

for palabra in vocabulario_B:

    if palabra in vocabulario_C:
        compartidas_BC += [palabra]


print("\n")
print("PALABRAS COMPARTIDAS")

print("A y B:", len(compartidas_AB))
print("A y C:", len(compartidas_AC))
print("B y C:", len(compartidas_BC))


#####################################################################################
####    Cinco palabras exclusivas por documento

exclusivas_A = []

for palabra in vocabulario_A:

    if palabra not in vocabulario_B and palabra not in vocabulario_C:
        exclusivas_A += [palabra]


exclusivas_B = []

for palabra in vocabulario_B:

    if palabra not in vocabulario_A and palabra not in vocabulario_C:
        exclusivas_B += [palabra]


exclusivas_C = []

for palabra in vocabulario_C:

    if palabra not in vocabulario_A and palabra not in vocabulario_B:
        exclusivas_C += [palabra]


print("\n")
print("CINCO PALABRAS EXCLUSIVAS")

print("Documento A:", exclusivas_A[:5])
print("Documento B:", exclusivas_B[:5])
print("Documento C:", exclusivas_C[:5])

print("Tamaño del vocabulario general:", len(vocabulario_general))

PALABRA_1 = "inteligencia"
PALABRA_2 = "medio"

palabras, matriz, reducida, pca = ejercicio_3(vocabulario_general, PALABRA_1, PALABRA_2)


##############################################################


# ============================================================================
# CELDA 4.0 - VERIFICACIÓN (ejecutar DESPUÉS de las celdas de los ejercicios 1, 2 y 3)
# El ejercicio 4 no vuelve a definir nada de los ejercicios anteriores: usa las
# funciones de las prácticas y los vocabularios que ya existen en el notebook.
# ===============================================================================
import numpy as np

requeridos = [
    "AMinusculas", "tokenizador3", "eliminador_stopwords", "lematizar", "leer_texto",
    "vocabulario_A", "vocabulario_B", "vocabulario_C", "vocabulario_general"
]

faltantes = []

for nombre in requeridos:

    if nombre not in globals():
        faltantes += [nombre]

if len(faltantes) > 0:
    print("FALTA definir (o tiene otro nombre en el notebook):", faltantes)

else:
    # El ejercicio 4 necesita posiciones, por eso vocabulario_general debe ser lista
    # (misma condición que pide la celda del ejercicio 3)
    if type(vocabulario_general) != list:
        vocabulario_general = list(vocabulario_general)

    print("Todo listo para el ejercicio 4.")
    print("Tamaño del vocabulario general:", len(vocabulario_general))


# %% ============================================================================
# EJERCICIO 4 a) Procesar el mensaje con la misma secuencia del ejercicio 1
# ===============================================================================

#### Misma secuencia del ejercicio 1, con las funciones de las prácticas:
#### minusculas -> tokenizacion -> eliminacion de stopwords -> lematizacion
def procesar_p4(texto):

    texto = AMinusculas(texto)

    tokens_iniciales = tokenizador3(texto)

    tokens_sin_stopwords = eliminador_stopwords(tokens_iniciales)

    tokens_lematizados = lematizar(tokens_sin_stopwords)

    return tokens_iniciales, tokens_sin_stopwords, tokens_lematizados


texto_mensaje = leer_texto("textod.txt")

iniciales_M, sin_stop_M, tokens_M = procesar_p4(texto_mensaje)

print("=" * 90)
print("EJERCICIO 4 a)")
print("=" * 90)
print("Número de tokens iniciales:                   ", len(iniciales_M))
print("Número de tokens después de eliminar stopwords:", len(sin_stop_M))
print("Número de tokens después de lematizar:         ", len(tokens_M))
print("Primeros 15 tokens del resultado final:", tokens_M[0:15])
print("Resultado final completo:", tokens_M)


# ============================================================================
# EJERCICIO 4 b) Puntajes por tema y clasificación automática
# ===============================================================================

#### Cuenta cuántos tokens del texto aparecen en un vocabulario
def contar_coincidencias(tokens, vocabulario):

    coincidencias = 0

    for token in tokens:

        if token in vocabulario:
            coincidencias += 1

    return coincidencias


#### Calcula los tres puntajes y asigna el tema con mayor puntaje
def clasificar(tokens):

    puntaje_A = contar_coincidencias(tokens, vocabulario_A)
    puntaje_B = contar_coincidencias(tokens, vocabulario_B)
    puntaje_C = contar_coincidencias(tokens, vocabulario_C)

    tema = "A (Inteligencia artificial)"
    mayor = puntaje_A

    if puntaje_B > mayor:
        tema = "B (Medio ambiente)"
        mayor = puntaje_B

    if puntaje_C > mayor:
        tema = "C (Finanzas personales)"
        mayor = puntaje_C

    return puntaje_A, puntaje_B, puntaje_C, tema


puntaje_A, puntaje_B, puntaje_C, tema = clasificar(tokens_M)

print("=" * 90)
print("EJERCICIO 4 b)")
print("=" * 90)
print("puntaje_A:", puntaje_A)
print("puntaje_B:", puntaje_B)
print("puntaje_C:", puntaje_C)
print("Tema asignado automáticamente:", tema)


# ============================================================================
# EJERCICIO 4 c) Vector de frecuencias con vocabulario_general
# ===============================================================================

#### Cada posición del vector es la frecuencia de la palabra del vocabulario
def vector_frecuencias(tokens, vocabulario):

    vector = np.zeros(len(vocabulario), dtype=int)

    for token in tokens:

        if token in vocabulario:
            posicion = vocabulario.index(token)
            vector[posicion] += 1

    return vector


#### Cuenta las posiciones con frecuencia mayor que cero
def contar_positivos(vector):

    positivos = 0

    for valor in vector:

        if valor > 0:
            positivos += 1

    return positivos


#### Obtiene las n palabras con mayor frecuencia (sin ordenar con funciones hechas)
def palabras_mas_frecuentes(vector, vocabulario, n):

    copia = np.copy(vector)
    palabras = []
    frecuencias = []

    for k in range(n):

        posicion_mayor = 0

        for i in range(len(copia)):

            if copia[i] > copia[posicion_mayor]:
                posicion_mayor = i

        palabras += [vocabulario[posicion_mayor]]
        frecuencias += [int(copia[posicion_mayor])]

        copia[posicion_mayor] = -1

    return palabras, frecuencias


vector_M = vector_frecuencias(tokens_M, vocabulario_general)

palabras_top, frecuencias_top = palabras_mas_frecuentes(vector_M, vocabulario_general, 5)

print("=" * 90)
print("EJERCICIO 4 c)")
print("=" * 90)
print("Longitud del vector:", len(vector_M))
print("Posiciones con frecuencia mayor que cero:", contar_positivos(vector_M))
print("Cinco palabras con mayor frecuencia:")

for i in range(len(palabras_top)):
    print("   ", palabras_top[i], "->", frecuencias_top[i])

print("Representación implementada: Bolsa de Palabras (Bag of Words, BoW)")



# ============================================================================
# EJERCICIO 4 d) Sustituir dinero->capital, gastos->desembolsos, ahorrar->reservar
# ===============================================================================

#### Sustituye palabras del texto original y lo reconstruye (sin replace ni join)
def sustituir_palabras(texto, sustituciones):

    tokens = tokenizador3(AMinusculas(texto))

    texto_nuevo = ""

    for token in tokens:

        if token in sustituciones:
            token = sustituciones[token]

        texto_nuevo += token + " "

    return texto_nuevo


sustituciones = {
    "dinero": "capital",
    "gastos": "desembolsos",
    "ahorrar": "reservar"
}

texto_sustituido = sustituir_palabras(texto_mensaje, sustituciones)

# Se ejecuta otra vez TODO el sistema con el texto sustituido
iniciales_S, sin_stop_S, tokens_S = procesar_p4(texto_sustituido)

puntaje_A2, puntaje_B2, puntaje_C2, tema2 = clasificar(tokens_S)

print("=" * 90)
print("EJERCICIO 4 d)")
print("=" * 90)
print("Tokens finales con sustitución:", tokens_S)
print()
print("Puntaje      Original    Con sustitución")
print("puntaje_A   ", puntaje_A, "         ", puntaje_A2)
print("puntaje_B   ", puntaje_B, "         ", puntaje_B2)
print("puntaje_C   ", puntaje_C, "         ", puntaje_C2)
print()
print("Clasificación original:       ", tema)
print("Clasificación con sustitución:", tema2)

if tema == tema2:
    print("La clasificación se MANTIENE.")
else:
    print("La clasificación CAMBIA.")
