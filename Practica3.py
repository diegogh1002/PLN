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
####    Tokenizador
def tokenizador3(texto):
    tokens = []
    palabra = ""

    for caracter in texto:
        if caracter == " " or caracter == ".":
            if palabra != "":
                tokens.append(palabra)
                palabra = ""
        elif caracter not in string.punctuation and not caracter.isdigit():
            palabra += caracter

    if palabra != "":
        tokens.append(palabra)

    return tokens


#####################################################################################
####    Pasar a minusculas
def AMinusculas(texto):
    resultado = ""

    for caracter in texto:
        if "A" <= caracter <= "Z":
            resultado += chr(ord(caracter) + 32)
        elif caracter == "Á":
            resultado += "á"
        elif caracter == "É":
            resultado += "é"
        elif caracter == "Í":
            resultado += "í"
        elif caracter == "Ó":
            resultado += "ó"
        elif caracter == "Ú":
            resultado += "ú"
        else:
            resultado += caracter

    return resultado


#####################################################################################
####    Eliminador de stopwords
def eliminador_stopwords(tokens):

    stopwords = [
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

    tokens_sin_stopwords = []

    for token in tokens:
        if token not in stopwords:
            tokens_sin_stopwords.append(token)

    return tokens_sin_stopwords


#####################################################################################
####    Aplicar reglas de lematizacion
def aplicar_reglas(palabra):

    if palabra.endswith("ando"):
        return palabra[:-4] + "ar"

    elif palabra.endswith("iendo"):
        return palabra[:-5] + "er"

    elif palabra.endswith("es"):
        return palabra[:-2]

    elif palabra.endswith("s"):
        return palabra[:-1]

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

    return aplicar_reglas(palabra)


#####################################################################################
####    Lematizador
def lematizar(palabras):

    palabras_lematizadas = []

    for palabra in palabras:
        palabra_lematizada = lematizador_reglas_excepciones(palabra)
        palabras_lematizadas.append(palabra_lematizada)

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

    tokens_unicos = list(set(tokens))

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

contenido.append(
    Paragraph("PROCESANDO: " + "texto800.txt", estilos["Title"])
)

contenido.append(
    Paragraph("Texto original:", estilos["Heading2"])
)

contenido.append(
    Paragraph(texto.replace("\n", "<br/>"), estilos["BodyText"])
)

texto = AMinusculas(texto)

texto = tokenizador3(texto)

print(
    "Número de tokens (palabras antes de eliminar stop words): ",
    len(texto)
)

contenido.append(
    Paragraph(
        "Número de tokens antes de eliminar stop words: " + str(len(texto)),
        estilos["BodyText"]
    )
)

texto = eliminador_stopwords(texto)

print(
    "Número de tokens (palabras después de eliminar stop words): ",
    len(texto)
)

contenido.append(
    Paragraph(
        "Número de tokens después de eliminar stop words: " + str(len(texto)),
        estilos["BodyText"]
    )
)

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

contenido.append(
    Paragraph(
        "Tokenizado y lematizado:",
        estilos["Heading2"]
    )
)

contenido.append(
    Paragraph(
        " ".join(texto),
        estilos["BodyText"]
    )
)

contenido.append(
    Paragraph(
        "Tiempo de ejecución: " + str(t_fin - t_ini) + " segundos",
        estilos["BodyText"]
    )
)

contenido.append(
    Paragraph(
        "Memoria pico: " + str(pico / 10**3) + " Kb",
        estilos["BodyText"]
    )
)

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
        palabra_lematizada = lematizar([palabra])[0]

        # Buscar la palabra lematizada
        if palabra_lematizada in vectores:
            print(f"Vector de la palabra '{palabra_lematizada}': "f"{vectores[palabra_lematizada]}")

        else:
            print(f"La palabra '{palabra_lematizada}' no existe en el documento.")
            # Crear un nuevo vector con una posición adicional
            vector_nuevo = [0] * (len(vectores) + 1)
            # Poner 1 en la ultima posición
            vector_nuevo[len(vectores)] = 1
            # Agregar 0 a los vectores que ya existían
            for palabra_existente in vectores:
                vectores[palabra_existente] = (vectores[palabra_existente] + [0])
            # Agregar la nueva palabra y su vector
            vectores[palabra_lematizada] = vector_nuevo
            print(f"Vector de la palabra agregada "f"'{palabra_lematizada}': "f"{vectores[palabra_lematizada]}")

    else:
        print("No se realizará la búsqueda de palabras en el documento.")
        break