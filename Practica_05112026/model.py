# ==========================================================
# PROGRAMA PRINCIPAL
# ==========================================================

from Practica_2720226.lematizador_regex.lematizador_regex import tokenizadoregex

documentos = ["texto01.txt", "texto02.txt", "texto03.txt"]

print("\n")
print("=" * 90)
print("RESULTADOS DE DATOS")
print("=" * 90)


for archivo in documentos:
    texto = tokenizadoregex(archivo)
    print("\n")
    print("-" * 90)
    print("ARCHIVO:", archivo)
    print("-" * 90)
    print("TEXTO TOKENIZADO:", texto)
    