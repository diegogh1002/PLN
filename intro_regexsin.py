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

def limpiar(token):
    # Quita signos de puntuación al inicio y al final del token
    signos = ".,;:“”\""

    while len(token) > 0 and token[0] in signos:
        token = token[1:]

    while len(token) > 0 and token[-1] in signos:
        token = token[0:-1]

    return token


def horas(tokens):
    horas = []

    for token in tokens:
        hora = limpiar(token)

        if len(hora) == 5 and hora[2] == ":" and hora[0:2].isnumeric() and hora[3:5].isnumeric():
            horas += [hora]

    return horas


def fechas(tokens):
    fechas = []

    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
             "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

    # Fechas numéricas: 05/10/2026 o 06-10-2026
    for token in tokens:
        fecha = limpiar(token)

        if len(fecha) == 10 and (fecha[2] == "/" or fecha[2] == "-") and fecha[5] == fecha[2]:
            if fecha[0:2].isnumeric() and fecha[3:5].isnumeric() and fecha[6:10].isnumeric():
                fechas += [fecha]

    # Fechas escritas: 5 de octubre de 2026
    for i in range(len(tokens) - 4):
        mes = limpiar(tokens[i + 2])
        anio = limpiar(tokens[i + 4])

        if tokens[i].isnumeric() and tokens[i + 1] == "de" and mes in meses and tokens[i + 3] == "de" and anio.isnumeric():
            fechas += [tokens[i] + " de " + mes + " de " + anio]

    return fechas


def telefonos(tokens):
    telefonos = []

    i = 0
    while i < len(tokens):
        telefono = ""
        digitos = 0
        j = i

        # Junta tokens seguidos que solo tengan dígitos, +, -, ( )
        while j < len(tokens):
            parte = limpiar(tokens[j])
            valido = len(parte) > 0

            for c in parte:
                if c.isnumeric():
                    digitos += 1
                elif c != "+" and c != "-" and c != "(" and c != ")":
                    valido = False

            if valido == False:
                break

            if telefono != "":
                telefono += " "
            telefono += parte
            j += 1

            # Si traía coma o punto, ahí termina el número
            if parte != tokens[j - 1]:
                break

        if digitos >= 10 and digitos <= 12 and telefono != "":
            telefonos += [telefono]
            i = j
        else:
            i += 1

    return telefonos


def correos(tokens):
    correos = []

    for token in tokens:
        correo = limpiar(token)
        arroba = False
        punto = False

        for c in correo:
            if c == "@":
                arroba = True
            elif c == "." and arroba:
                punto = True

        if arroba and punto:
            correos += [correo]

    return correos


# ==========================================================
# DIRECCIONES
# ==========================================================

def direcciones(tokens):
    direcciones = []
    abreviaturas = ["Av.", "Col.", "Depto.", "C.P."]

    for i in range(len(tokens)):

        if tokens[i] == "Calle" or tokens[i] == "Av.":
            direccion = tokens[i]

            for j in range(i + 1, len(tokens)):
                letra = tokens[j][0]

                # Palabra en minúscula (que no sea de/del): ya no es dirección
                if letra.isupper() == False and letra.isnumeric() == False and tokens[j] != "de" and tokens[j] != "del":
                    break

                direccion += " " + tokens[j]

                # Punto final (que no sea abreviatura)
                if tokens[j][-1] == "." and tokens[j] not in abreviaturas:
                    break

            direcciones += [limpiar(direccion)]

    return direcciones


# ==========================================================
# URLS
# ==========================================================

def urls(tokens):
    urls = []

    for token in tokens:
        url = limpiar(token)

        if url[0:8] == "https://":
            urls += [url]

    return urls


# ==========================================================
# NOMBRES
# ==========================================================

def nombres(tokens):
    nombres = []

    titulos = ["Dra.", "Mtra.", "Dr.", "Mtro."]
    palabras_no_nombre = ["Calle", "Alcaldía", "Parque"]

    for i in range(len(tokens) - 2):
        palabra1 = tokens[i]
        palabra2 = tokens[i + 1]
        palabra3 = limpiar(tokens[i + 2])

        valido = palabra1 not in palabras_no_nombre

        # Cada palabra: mayúscula inicial y el resto solo minúsculas
        for palabra in [palabra1, palabra2, palabra3]:
            if len(palabra) < 2 or palabra[0].isupper() == False:
                valido = False

            for c in palabra[1:]:
                if c.isupper() or c.isnumeric() or c in ".,-@()":
                    valido = False

        if valido:
            nombre = palabra1 + " " + palabra2 + " " + palabra3

            if i > 0 and tokens[i - 1] in titulos:
                nombre = tokens[i - 1] + " " + nombre

            nombres += [nombre]

    return nombres


# ==========================================================
# FOLIOS, CLAVES Y REFERENCIAS
# ==========================================================

def folios(tokens):
    folios = []

    for token in tokens:
        folio = limpiar(token)
        letras = 0
        numeros = 0
        guiones = 0
        valido = True

        for c in folio:
            if c.isupper():
                letras += 1
            elif c.isnumeric():
                numeros += 1
            elif c == "-":
                guiones += 1
            else:
                valido = False

        # Con guion (INC-2026-1048) o letras pegadas a números (HOGAR15)
        if valido and letras >= 1 and numeros >= 1 and (guiones >= 1 or letras >= 3):
            folios += [folio]

    return folios


# ==========================================================
# MONTOS
# ==========================================================

def montos(tokens):
    montos = []

    for i in range(len(tokens)):
        monto = limpiar(tokens[i])
        puntos = 0
        valido = len(monto) >= 5 and monto[0] == "$" and monto[-3] == "."

        for c in monto[1:]:
            if c == ".":
                puntos += 1
            elif c.isnumeric() == False and c != ",":
                valido = False

        if valido and puntos == 1:

            if i + 1 < len(tokens) and tokens[i + 1][0:3] == "MXN":
                monto += " MXN"

            montos += [monto]

    return montos


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

    #texto = AMinusculas(texto)

    texto = tokenizador3(texto)

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