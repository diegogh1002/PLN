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

    texto = eliminador_stopwords(texto)
    
    print("\n")
    print("-" * 90)
    print("ARCHIVO:", archivo)
    print("-" * 90)
    
    