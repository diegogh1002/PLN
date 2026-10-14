import string
import re
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

    if token != "":
        tokens += [token]

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

def horas(texto):
    # 08:35
    return re.findall(r"\b[0-9]{2}:[0-9]{2}\b", texto)


def fechas(texto):
    # 30/09/2026 o 06-10-2026
    fechas = re.findall(r"\b[0-9]{2}[/-][0-9]{2}[/-][0-9]{4}\b", texto)

    # 5 de octubre de 2026
    fechas += re.findall(r"\b[0-9]{1,2}\sde\s[a-z]+\sde\s[0-9]{4}\b", texto)

    return fechas


def telefonos(texto):
    # 55 7342 9816 / +52 55 6001 4478 / +52 (442) 310-8820 / 800-555-0199 / 01 800 700 2026
    telefonos = re.findall(r"\+?[0-9]{0,2}\s?\(?[0-9]{2,3}\)?[\s-][0-9]{3,4}[\s-][0-9]{4}\b", texto)

    # Quitamos el espacio que puede quedar al inicio
    for i in range(len(telefonos)):
        if telefonos[i][0] == " " or telefonos[i][0] == "\n":
            telefonos[i] = telefonos[i][1:]

    return telefonos


def correos(texto):
    # usuario@dominio.mx / nombre+etiqueta@dominio.com
     return re.findall(r"[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+.[a-z]\b", texto)


# ==========================================================
# DIRECCIONES
# ==========================================================

def direcciones(texto):
    # Desde "Calle" o "Av." hasta el código postal
    direcciones = re.findall(r"Calle\s[A-Za-zÁÉÍÓÚáéíóúñ0-9,.\s]+C.P.\s[0-9]{5}", texto)
    direcciones += re.findall(r"Av.\s[A-Za-zÁÉÍÓÚáéíóúñ0-9,.\s]+C.P.\s[0-9]{5}", texto)

    return direcciones


# ==========================================================
# URLS
# ==========================================================

def urls(texto):
    return re.findall(r"https://[a-zA-Z0-9./_-]+[a-zA-Z0-9]", texto)


# ==========================================================
# NOMBRES
# ==========================================================
def nombres(texto):
    
    nombres = re.findall(r"Dra.\s[A-ZÁÉÍÓÚ][a-záéíóúñ]+\s[A-ZÁÉÍÓÚ][a-záéíóúñ]+\s[A-ZÁÉÍÓÚ][a-záéíóúñ]\b", texto)
    
    nombres += re.findall(r"Mtra.\s[A-ZÁÉÍÓÚ][a-záéíóúñ]+\s[A-ZÁÉÍÓÚ][a-záéíóúñ]+\s[A-ZÁÉÍÓÚ][a-záéíóúñ]\b", texto)
    
    nombres += re.findall(r"\b[A-ZÁÉÍÓÚ][a-záéíóúñ]+\s[A-ZÁÉÍÓÚ][a-záéíóúñ]+\s[A-ZÁÉÍÓÚ][a-záéíóúñ]+\b", texto)
    return nombres


# ==========================================================
# FOLIOS, CLAVES Y REFERENCIAS
# ==========================================================

def folios(texto):
    # INC-2026-1048, CJ-88-A, PC-SOP-17
    folios = re.findall(r"\b[A-Z]+-[A-Z0-9]+-[A-Z0-9]+\b", texto)

    # HOGAR15
    folios += re.findall(r"\b[A-Z]{3,}[0-9]\b", texto)

    return folios


# ==========================================================
# MONTOS
# ==========================================================

def montos(texto):
    # $18,450.00 MXN
    return re.findall(r"\$[0-9,]+\.[0-9]{2}\sMXN", texto)


# ==========================================================
# PROGRAMA PRINCIPAL
# ==========================================================

archivos = ["texto01.txt", "texto02.txt", "texto03.txt"]

print("\n")
print("=" * 90)
print("RESULTADOS DE DATOS")
print("=" * 90)

for archivo in archivos:

    texto = leer_texto(archivo)

    #texto = AMinusculas(texto)

    #texto = tokenizador3(texto)

    print("\n")
    print("-" * 90)
    print("ARCHIVO:", archivo)
    print("-" * 90)

    #print("Tokens:")
    #print(texto)

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

    print("\nNombres encontrados:")
    print(nombres(texto))

    print("\nFolios, claves y referencias encontradas:")
    print(folios(texto))

    print("\nMontos encontrados:")
    print(montos(texto))