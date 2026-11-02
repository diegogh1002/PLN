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

    if re.search(r"\W",texto[-1]):
        texto = texto + '.'

    tokens = re.findall(r"(?:\w|\d|[-/_@:\.])+", texto)

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

    if re.search(r"es$", palabra) and n > 3:
        return palabra[0:n-2]

    if re.search(r"s$", palabra) and n > 1:
        return palabra[0:n-1]

    if re.search(r"é$", palabra) and n > 4:
        return palabra[0:n-1]

    if re.search(r"á$", palabra) and n > 4:
        return palabra[0:n-1]
    
    if re.search(r"(\.|,)$", palabra):
        palabra = re.search(r"((?:\w|\d|[-/_@:\.])?+(?:\w|\d))|\w", palabra).group()

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
def leer_texto(nombre_archivo):
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        texto = archivo.read()
    return texto

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

    texto = tokenizador3(texto)
    
    texto = ciclo_AMinusculas(texto)
    
    texto = lematizar(texto)

    
    print("\n")
    print("-" * 90)
    print("ARCHIVO:", archivo)
    print("-" * 90)

    