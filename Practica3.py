import string

from lemas_excepciones import lemas_excepciones

# ### medir consumo de memoria y tiempo
import time
import tracemalloc

# ### para generar pdf
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


#####################################################################################
####    Tokenizador de palabras
def tokenizador3(texto):

    tokens = []
    token = ""

    delimiters = string.whitespace + string.punctuation + string.digits

    if texto == "":
        return tokens

    if texto[-1] != ' ' and texto[-1] != '.':
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
def AMinusculas(texto):

    letras = ''

    for letra in texto:

        if ord(letra) >= 65 and ord(letra) <= 90:
            letra = chr(ord(letra) + 32)

        elif ord(letra) in [193, 201, 205, 211, 218]:
            letra = chr(ord(letra) + 32)

        letras += letra

    return letras


#####################################################################################
####    Eliminador de Stop Words
def eliminador_stopwords(tokens):

    stop_words = [
        "a", "al", "algo", "algunas", "algunos", "ante", "antes", "como",
        "con", "contra", "cual", "cuando", "de", "del", "desde", "donde",
        "durante", "e", "el", "ella", "ellas", "ellos", "en", "entre",
        "era", "eran", "es", "esa", "esas", "ese", "eso", "esos", "esta",
        "estas", "este", "esto", "estos", "fue", "fueron", "ha", "han",
        "hasta", "la", "las", "le", "les", "lo", "los", "más", "me",
        "mi", "mis", "muy", "no", "nos", "nosotros", "o", "para", "pero",
        "por", "que", "qué", "se", "sea", "ser", "si", "sí", "sin",
        "sobre", "son", "su", "sus", "también", "te", "tiene", "tienen",
        "tu", "tus", "un", "una", "uno", "unos", "y", "ya", "yo"
    ]

    tokens_nuevos = []

    for token in tokens:

        if token not in stop_words:
            tokens_nuevos += [token]

    return tokens_nuevos


#####################################################################################
####    Aplicar reglas de lematizacion
def aplicar_reglas(palabra):

    n = len(palabra)

    if palabra[n-5:n] == "ando" and n > 5:
        return palabra[0:n-5] + "ar"

    elif palabra[n-6:n] == "iendo" and n > 6:
        return palabra[0:n-6] + "er"

    elif palabra[n-2:n] == "es" and n > 3:
        return palabra[0:n-2]

    elif palabra[n-1:n] == "s" and n > 1:
        return palabra[0:n-1]

    elif palabra.endswith("aron"):
        return palabra[:-4] + "ar"

    elif palabra.endswith("ieron"):
        return palabra[:-5] + "er"

    elif palabra.endswith("aremos"):
        return palabra[:-6] + "ar"

    elif palabra.endswith("eremos"):
        return palabra[:-6] + "er"

    elif palabra.endswith("iremos"):
        return palabra[:-6] + "ir"

    elif palabra.endswith("ará"):
        return palabra[:-3] + "ar"

    elif palabra.endswith("erá"):
        return palabra[:-3] + "er"

    elif palabra.endswith("irá"):
        return palabra[:-3] + "ir"

    elif palabra.endswith("aste"):
        return palabra[:-4] + "ar"

    elif palabra.endswith("iste"):
        return palabra[:-4] + "ir"

    elif palabra.endswith("aban"):
        return palabra[:-4] + "ar"

    elif palabra.endswith("ían"):
        return palabra[:-3] + "er"

    else:
        return palabra


#####################################################################################
####    Lematizador con excepciones
def lematizador_reglas_excepciones(palabra):

    if palabra in lemas_excepciones:
        return lemas_excepciones[palabra]

    else:
        return aplicar_reglas(palabra)


#####################################################################################
####    Lematizar
def lematizar(palabras):

    palabras_lematizadas = [None] * len(palabras)

    for i in range(len(palabras)):

        palabra_lematizada = lematizador_reglas_excepciones(palabras[i])

        palabras_lematizadas[i] = palabra_lematizada

    return palabras_lematizadas


#####################################################################################
####    Leer texto de un archivo
def leer_texto(nombre_archivo):

    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        texto = archivo.read()

    return texto


#####################################################################################
####    One Hot Encoding
def one_hot_encoding(tokens):

    tokens_unicos = []

    for token in tokens:

        if token not in tokens_unicos:
            tokens_unicos += [token]

    vectors = {}

    for token in tokens_unicos:

        vector = [0] * len(tokens_unicos)

        index = tokens_unicos.index(token)

        vector[index] = 1

        vectors[token] = vector

    return vectors


#####################################################################################
####    Procesar archivo

pdf = SimpleDocTemplate("texto800.pdf", pagesize=letter)

estilos = getSampleStyleSheet()

contenido = []

tracemalloc.start()

t_ini = time.time()

texto = leer_texto("texto800.txt")

print("\n" + "=" * 90)
print("PROCESANDO:", "texto800.txt")
print("=" * 90)

contenido += [
    Paragraph("PROCESANDO: texto800.txt", estilos["Title"]),
    Paragraph("Texto original:", estilos["Heading2"]),
    Paragraph(texto.replace("\n", "<br/>"), estilos["BodyText"])
]

texto = AMinusculas(texto)

texto = tokenizador3(texto)

print(
    "Número de tokens (palabras antes de eliminar stop words): ",
    len(texto)
)

contenido += [
    Paragraph(
        "Número de tokens antes de eliminar stop words: " + str(len(texto)),
        estilos["BodyText"]
    )
]

texto = eliminador_stopwords(texto)

print(
    "Número de tokens (palabras después de eliminar stop words): ",
    len(texto)
)

contenido += [
    Paragraph(
        "Número de tokens después de eliminar stop words: " + str(len(texto)),
        estilos["BodyText"]
    )
]

texto = lematizar(texto)

vectores = one_hot_encoding(texto)

t_fin = time.time()

actual, pico = tracemalloc.get_traced_memory()

print(
    "El tiempo de ejecución fue de:",
    t_fin - t_ini,
    "segundos"
)

print(
    "La memoria pico fue de:",
    pico / 10**3,
    "Kb"
)

print(
    "La memoria actual es de:",
    actual / 10**3,
    "Kb"
)

contenido += [
    Paragraph("Tokenizado y lematizado:", estilos["Heading2"]),
    Paragraph(" ".join(texto), estilos["BodyText"]),
    Paragraph(
        "Tiempo de ejecución: " + str(t_fin - t_ini) + " segundos",
        estilos["BodyText"]
    ),
    Paragraph(
        "Memoria pico: " + str(pico / 10**3) + " Kb",
        estilos["BodyText"]
    )
]

tracemalloc.stop()

pdf.build(contenido)


#####################################################################################
####    Buscar palabra

while True:

    print("¿Desea saber si existe una palabra en el documento? (s/n): ")

    respuesta = input().lower()

    if respuesta == "s":

        palabra = input("Ingrese la palabra a buscar: ")

        palabra = AMinusculas(palabra)

        palabra = tokenizador3(palabra)

        if len(palabra) > 0:

            palabra_lematizada = lematizar(palabra)[0]

            if palabra_lematizada in vectores:

                print(
                    f"Vector de la palabra lematizada '{palabra_lematizada}': "
                    f"{vectores[palabra_lematizada]}"
                )

            else:

                vector_nuevo = [0] * (len(vectores) + 1)

                vector_nuevo[len(vectores)] = 1

                for palabra_existente in vectores:

                    vectores[palabra_existente] = (
                        vectores[palabra_existente] + [0]
                    )

                vectores[palabra_lematizada] = vector_nuevo

                print(
                    f"Vector de la palabra lematizada agregada "
                    f"'{palabra_lematizada}': "
                    f"{vectores[palabra_lematizada]}"
                )

        else:

            print("No se encontró una palabra válida para buscar.")

    else:

        print("No se realizará la búsqueda de palabras en el documento.")

        break
