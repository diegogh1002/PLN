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
####    Main

texto = """..VOy a la rÉpRob4#$#$#546ar / % . el S6#%#5í. 6 88808 no .... Es#%#53t678uDio PLN...979

H0L4!! La CIENCIA de D4T0S permite analizar información!!! Los estudiantes están estudiando programación, mientras los profesores están explicando conceptos importantes. 12345 ###

L@s alumn0s están trabajand0 con Python!!! Algunos están investigando algoritmos, otros están desarrollando aplicaciones... La información contiene errores como d@t0s, pr0gram4ción, an4lisis y c0nocimiento.

ÁRBOL árbol ÁRB0L... CIENCIA ciencia C1ENCIA... MÉXICO méxico M3XIC0... INFORMACIÓN informaci0n INFORM4CIÓN!!!

Estudiando, caminando, trabajando, programando, aprendiendo, comiendo, escribiendo y leyendo. Casas, libros, árboles, estudiantes, profesores, computadoras, programas, modelos, algoritmos, datos, sistemas.

@@@ ### $$$ %%% &&& /// +++ === *** !!! ??? ... 123 456 789 2026 98765.

El estudiante está leyendo un documento y está escribiendo información para su proyecto. La computadora está ejecutando instrucciones, mientras el programa está eliminando palabras que no aportan información relevante.

Los modelos están aprendiendo de los datos. Las empresas están utilizando inteligencia artificial para mejorar sus procesos. Los analistas están buscando soluciones y los investigadores están estudiando diferentes métodos.

c4s4s libr0s estudi4ntes pr0fesores c0mputadoras alg0ritmos inf0rmación s0luciones resultad0s.

El texto contiene palabras repetidas, repetidas, repetidas!!! También contiene frases con espacios     múltiples y signos... como estos!!!

¿El programa puede identificar correctamente las palabras? ¿Puede eliminar los números? ¿Puede transformar las letras mayúsculas? ¿Puede eliminar las palabras de la lista de Stop Words?

Finalmente, los estudiantes están preparando sus experimentos, analizando información, comparando resultados y realizando pruebas. FIN DE LA PRUEBA!!! 2026 ### @@@"""



print("Original: ", texto)
tracemalloc.start()
t_ini = time.time()
texto = AMinusculas(texto)
texto = tokenizador3(texto)
print("Número de tokens (palabras antes de eliminar stop words): ", len(texto))
texto = eliminador_stopwords(texto)
print("Número de tokens (palabras después de eliminar stop words): ", len(texto))
t_fin = time.time()
actual, pico = tracemalloc.get_traced_memory()
print("El tiempo de ejecución fue de:", t_fin - t_ini, "segundos")
print("La memoria pico fue de:", pico / 10**3, "Kb")
print("La memoria actual es de:", actual / 10**3, "Kb")
print("Tokenizado: ", texto)
