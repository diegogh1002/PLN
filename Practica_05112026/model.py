from lematizador_regex.lematizador_regex import tokenizadoregex
import time
import numpy as np
from sklearn.naive_bayes import MultinomialNB


#===================================================================
def eliminador_palabras_repetidas(vector):
    vectoraux = [vector[0]]
    for palabra in vector:
        if palabra not in vectoraux:
            vectoraux+= [palabra]
    return vectoraux

#===================================================================
def matriz_bag_words(corpus, vector_unico):
    num_doc_corpus = len(corpus)
    num_doc_vector = len(vector_unico)
    matriz_bow = np.zeros((len(corpus), len(vector_unico)), dtype=int)

    for i in range(num_doc_corpus):
        #Cuantas veces se repite la palabra en el documento
        j = 0
        for pal_unico in vector_unico:
            for palabra in corpus[i]:
                if palabra == pal_unico:
                    matriz_bow[i][j] = matriz_bow[i][j] + 1
            j += 1
    return matriz_bow




#==================================================================
documentos_train = ["doc001.txt", "doc002.txt", "doc111.txt", "doc112.txt", "doc221.txt", "doc222.txt", "doc331.txt", "doc332.txt", "doc441.txt", "doc442.txt"]
corpus = []

for archivo in documentos_train:
    doctokenizado = tokenizadoregex(archivo)
    #print("TEXTO TOKENIZADO:", doctokenizado)
    corpus += [doctokenizado]

print("CORPUS:", corpus)

corpus_entrenamiento = []
for i in range(len(corpus)):
    corpus_entrenamiento += corpus[i]
    
vector_unico = eliminador_palabras_repetidas(corpus_entrenamiento)
print("VECTOR UNICO:", vector_unico)

X = matriz_bag_words(corpus, vector_unico)
print("MATRIZ BAG OF WORDS:", X)

#Vector de etiquetas
y = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]  # Etiquetas para cada documento
nombres_clases = ["deportes", "tecnologia", "cocina", "salud", "economia"]


#Cargar Modelo
modelo = MultinomialNB()
#Entrenamos Modelo
modelo.fit(X, y)

documentos_prueba = ["doc003.txt", "doc113.txt", "doc223.txt", "doc333.txt", "doc443.txt"]

for documento in documentos_prueba:
    documento_tokenizado = tokenizadoregex(documento)
    nuevo_vector = np.zeros((1, len(vector_unico)), dtype=int)
    
    for j,palabra in enumerate(vector_unico):
        if palabra in documento_tokenizado:
            nuevo_vector[0][j] += 1

#Predicción de la categoría del documento
    prediccion = modelo.predict(nuevo_vector)
    print(f"Documento: {documento}, Predicción de categoría: {prediccion[0]}-{nombres_clases[prediccion[0]]}")