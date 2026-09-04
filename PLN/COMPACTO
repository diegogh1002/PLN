import string

# ### medir consumo de memoria y tiempo
import time
import tracemalloc

def tokenizador3(texto):

    tracemalloc.start()
    t_ini = time.time()

    tokens = []
    token = ""

    delimiters = string.whitespace + string.punctuation + string.digits

    stop_words = ["el", "que", "la", "lo", "los", "las", "de", "del", "en", "a", "un", "uno", "es", "con", "para", "se", "al"]

    if texto[-1] != ' ' and texto[-1] != '.':
        texto = texto + '.'

    for i in range(0, len(texto)):

        letra = texto[i]

        # Mayúsculas a minúsculas
        if ord(letra) >= 65 and ord(letra) <= 90:
            letra = chr(ord(letra) + 32)

        elif ord(letra) in [193, 201, 205, 211, 218]:
            letra = chr(ord(letra) + 32)

        # Tokenización
        if letra == ' ' or letra == '.':
            if token != "":
                if token not in stop_words:
                    tokens += [token]
                token = ""

        else:
            if letra not in delimiters:
                token = token + letra

    t_fin = time.time()
    actual, pico = tracemalloc.get_traced_memory()

    print("Tiempo:", t_fin - t_ini, "segundos")
    print("Memoria pico:", pico / 10**3, "Kb")
    print("Memoria actual:", actual / 10**3, "Kb")
    print("Tokenizado:", tokens)

    return tokens



texto = "..VOy a la rÉpRob4#$#$#546ar / % . el S6#%#5í. 6 88808 no .... Es#%#53t678uDio PLN...979"

print("Original:", texto)
texto = tokenizador3(texto)