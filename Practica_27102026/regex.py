import string
import re
from lemas_excepciones import lemas_excepciones
import time
import tracemalloc


def leer_texto(nombre_archivo):
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        texto = archivo.read()

    return texto


# ===============================================================
# DATOS ESPECIALES
# ==========================================================

def horas(texto):
    # 08:35
    return re.findall(r"\b[0-9]{2}:[0-9]{2}\b", texto)


def fechas(texto):
    return re.findall(r"((?:\b[0-9]{2}[/-][0-9]{2}[/-][0-9]{4}\b)|(?:\b[0-9]{1,2}\sde\s[a-z]+\sde\s[0-9]{4}\b))", texto)

def telefonos(texto):
    # 55 7342 9816 / +52 55 6001 4478 / +52 (442) 310-8820 / 800-555-0199 / 01 800 700 2026
    telefonos = re.findall(r"[+]?[0-9]{0,2}\s?[(]?[0-9]{2,3}[)]?[\s-][0-9]{3,4}[\s-][0-9]{4}\b", texto)
    return telefonos


def correos(texto):
    # usuario@dominio.mx / nombre+etiqueta@dominio.com
     return re.findall(r"[\w.+-]+@[\w.-]+[.]\w+", texto)


# ============================================================================
# DIRECCIONES
# ==========================================================

def direcciones(texto):
    # Desde "Calle" o "Av." hasta el código postal
    direcciones = re.findall(r"Calle\s[\w,.\s]+[C.P.]\s[0-9]{5}", texto)
    direcciones += re.findall(r"Av.\s[\w,.\s]+[C.P.]\s[0-9]{5}", texto)

    return direcciones


# ==========================================================
# URLS
# =========================================================================

def urls(texto):
    return re.findall(r"https://[\w./_-]+[\w]", texto)


# ==========================================================
# NOMBRES
# ==========================================================
def nombres(texto):
    
    nombres1 = re.findall(r"Dra[.]\s[A-ZÁÉÍÓÚ]\w+\s[A-ZÁÉÍÓÚ]\w+\s[A-ZÁÉÍÓÚ]\w+\b", texto)
    nombres1 += re.findall(r"Mtra[.]\s[A-ZÁÉÍÓÚ]\w+\s[A-ZÁÉÍÓÚ]\w+\s[A-ZÁÉÍÓÚ]\w+\b", texto)
    nombres1 += re.findall(r"\b[A-ZÁÉÍÓÚ]\w+\s[A-ZÁÉÍÓÚ]\w+\s[A-ZÁÉÍÓÚ]\w+\b", texto)
    
    nombres = []
    for nombre in nombres1:
        if re.findall(r"\bAv\b", nombre) or re.findall(r"\bCalle\b", nombre) or re.findall(r"\bAlcaldía\b", nombre) or re.findall(r"\bParque\b", nombre):
            continue
        else:
            nombres += [nombre]
    return nombres


# ==========================================================
# FOLIOS, CLAVES Y REFERENCIAS
# =====================================================================================0

def folios(texto):
    # INC-2026-1048, CJ-88-A, PC-SOP-17
    folios = re.findall(r"\b[A-Z]+-[-?\w]+\b", texto)

    # HOGAR15
    folios += re.findall(r"\b[A-Z]{3,}[0-9]+\b", texto)

    return folios
# =====================================================================
# MONTOS
# ==========================================================

def montos(texto):
    # $18,450.00 MXN
    return re.findall(r"[$][0-9,?]+[.][0-9]{2}\s?MXN", texto)


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
    #horas(texto)
    
    print("\nFechas encontradas:")
    print(fechas(texto))
    #fechas(texto)
    
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