import string

from lemas_excepciones import lemas_excepciones
# ### medir consumo de memoria y tiempo
import time
import tracemalloc


#####################################################################################
####    Tokenizador de palabras
def tokenizador3(texto):

    tokens = []
    token = "" 
    
    delimiters = string.whitespace + string.punctuation + string.digits

    if texto[-1] != ' ' and texto[-1] != '.' and texto[-1] != '\n' and texto[-1] != '\r' and texto[-1] != '\t':
        texto = texto + '.'
        

    for i in range(0, len(texto)):

        if (texto[i] == ' ' or texto[i] == '\n' or texto[i] == '\r' or texto[i] == '\t' or texto[i] == ':' or texto[i] == '-' or texto[i] == '@'):
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
####    hora

def horas(tokens):
    horas = []

    for token in tokens:
        hora = ""

        for i in range(len(token)):
            if token[i].isnumeric():
                hora += token[i]
            elif token[i] == ":":
                hora += token[i]
            else:
                hora = ""
            if len(hora) == 5 and token[i]+1 == "h":
                horas += [hora]
                hora = ""
    return horas
    
#####################################################################################
####    fecha

def fechas(tokens):
    fechas = []

    for token in tokens:
        fecha = ""

        if token.isnumeric():
            fecha += token
        elif token == "de" or token == "del":
            fecha += token
        elif token == "enero" or token == "febrero" or token == "marzo" or token == "abril" or token == "mayo" or token == "junio" or token == "julio" or token == "agosto" or token == "septiembre" or token == "octubre" or token == "noviembre" or token == "diciembre":
            fecha += token
        elif token == "/" or token == "-":
            fecha += token
        if len(fecha) >= 5:
            fechas += [fecha]

    return fechas


#####################################################################################
####    telefonos

def telefonos(tokens):
    telefonos = []

    for token in tokens:
        telefono = ""

        if token.isnumeric():
            telefono += token
        elif token == "+" or token == "(" or token == ")" or token == "-":
            telefono += token
        if len(telefono) >= 10:
            telefonos += [telefono]

    return telefonos

#####################################################################################
####    correos

def correos(tokens):
    correos = []

    for i in range(len(tokens) - 2):

        if tokens[i+1] == "@":
            correo = tokens[i] + tokens[i+1] + tokens[i+2]
            correos += [correo]

    return correos   


#####################################################################################
####    Main

#texto = "..VOy a la rÉpRob4#$#$#546ar / % . el  S6#%#5í.  6  88808 no .... Es#%#53t678uDio PLN...979"

archivos = ["texto01.txt", "texto02.txt", "texto03.txt"]

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
    print("Original: ", texto)

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

    t_fin = time.time()
    actual, pico = tracemalloc.get_traced_memory()

    print("El tiempo de ejecución fue de:", t_fin - t_ini, "segundos")
    print("La memoria pico fue de:", pico / 10**3, "Kb")
    print("La memoria actual es de:", actual / 10**3, "Kb")
    print("Tokenizado y lematizado: ", texto)

    tracemalloc.stop()