import string
from lemas_excepciones import lemas_excepciones
import time
import tracemalloc


def tokenizador3(texto):
    tokens = []
    token = ""

    delimiters = string.whitespace 

    if texto[-1] != ' ' and texto[-1] != '.' and texto[-1] != '\n' and texto[-1] != '\r' and texto[-1] != '\t':
        texto = texto + '.'

    for i in range(0, len(texto)):
        if (texto[i] == ' ' or texto[i] == '\n' or texto[i] == '\r' or texto[i] == '\t'):
            if token != "":
                tokens += [token]
                token = ""
        else:
            if texto[i] not in delimiters:
                token = token + texto[i]

    return tokens


def AMinusculas(texto):
    letras = ''

    for letra in texto:
        if ord(letra) >= 65 and ord(letra) <= 90:
            letra = chr(ord(letra) + 32)

        elif ord(letra) in [193, 201, 205, 211, 218]:
            letra = chr(ord(letra) + 32)

        letras += letra

    return letras


def eliminador_stopwords(tokens):
    stop_words = ["el", "que", "la", "lo", "los", "las",
                  "de", "del", "en", "a", "un", "uno",
                  "es", "con", "para", "se", "al"]

    tokens_nuevos = []

    for token in tokens:
        if token not in stop_words:
            tokens_nuevos += [token]

    return tokens_nuevos


def aplicar_reglas(palabra):
    n = len(palabra)

    if palabra[n-5:n] == "ando" and n > 5:
        return palabra[0:n-5] + "ar"

    if palabra[n-6:n] == "iendo" and n > 6:
        return palabra[0:n-6] + "er"

    if palabra[n-2:n] == "es" and n > 3:
        return palabra[0:n-2]

    if palabra[n-1:n] == "s" and n > 1:
        return palabra[0:n-1]

    if palabra[n-4:n] == "aron" and n > 5:
        return palabra[0:n-4] + "ar"

    if palabra[n-5:n] == "ieron" and n > 6:
        return palabra[0:n-5] + "er"

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


def lematizador_reglas_excepciones(palabra):
    if palabra in lemas_excepciones:
        return lemas_excepciones[palabra]

    else:
        return aplicar_reglas(palabra)


def lematizar(palabras):
    texto_lematizado = [None] * len(palabras)

    for i in range(len(palabras)):
        palabra_lematizada = lematizador_reglas_excepciones(palabras[i])
        texto_lematizado[i] = palabra_lematizada

    return texto_lematizado


def leer_texto(nombre_archivo):
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        texto = archivo.read()

    return texto


# ==========================================================
# DATOS ESPECIALES
# ==========================================================

def horas(tokens):
    horas = []

    for token in tokens:
        hora = ""

        for i in range(len(token)):
            if token[i].isnumeric() or token[i] == "+":
                hora += token[i]

            elif token[i] == ":":
                hora += token[i]

            else:
                hora = ""

        if len(hora) == 5:
            horas += [hora]

    return horas


def fechas(tokens):
    fechas = []

    for token in tokens:
        fecha = ""

        for i in range(len(token)):
            if token[i].isnumeric():
                fecha += token[i]

            elif token[i] == "/" or token[i] == "-":
                fecha += token[i]

            else:
                fecha = ""

        if len(fecha) == 10:
            fechas += [fecha]

    return fechas


def telefonos(tokens):
    telefonos = []

    for i in range(len(tokens) - 2):
        telefono = ""

        if tokens[i].isnumeric() and tokens[i + 1].isnumeric() and tokens[i + 2].isnumeric():
            telefono = tokens[i] + tokens[i + 1] + tokens[i + 2]

        elif tokens[i][0] == "+":
            telefono = tokens[i] + tokens[i + 1] + tokens[i + 2]

        if len(telefono) >= 10:
            telefonos += [telefono]

    return telefonos


def correos(tokens):
    correos = []

    for token in tokens:
        correo = ""

        for i in range(len(token)):
            correo += token[i]

        if "@" in correo and "." in correo:
            correos += [correo]

    return correos


def direcciones(tokens):
    direcciones = []

    for i in range(len(tokens) - 1):
        direccion = ""

        if tokens[i] == "calle" or tokens[i] == "av." or tokens[i] == "col." or tokens[i] == "depto.":
            direccion = tokens[i] + " " + tokens[i+1]

        if tokens[i] == "c.p." and tokens[i+1].isnumeric() and len(tokens[i+1]) == 5:
            direccion = tokens[i] + " " + tokens[i+1]

        if len(direccion) >= 3:
            direcciones += [direccion]

    return direcciones


def urls(tokens):
    urls = []

    for token in tokens:
        url = ""

        for i in range(len(token)):
            url += token[i]

        if len(url) >= 8:
            if url[0:8] == "https://":
                urls += [url]

    return urls


# ==========================================================
# PROGRAMA PRINCIPAL
# ==========================================================

archivos = ["texto01.txt", "texto02.txt", "texto03.txt"]

print("\n")
print("=" * 90)
print("RESULTADOS DE DATOS ESPECIALES")
print("=" * 90)

for archivo in archivos:

    texto = leer_texto(archivo)

    texto = AMinusculas(texto)

    texto = tokenizador3(texto)

    print("\n")
    print("-" * 90)
    print("ARCHIVO:", archivo)
    print("-" * 90)

    print("Tokens:")
    print(texto)

    print("\nHoras encontradas:")
    print(horas(texto))

    print("\nFechas encontradas:")
    print(fechas(texto))

    print("\nTeléfonos encontrados:")
    print(telefonos(texto))

    print("\nCorreos encontrados:")
    print(correos(texto))

    print("\nDirecciones encontradas:")
    print(direcciones(texto))

    print("\nURLs encontradas:")
    print(urls(texto))