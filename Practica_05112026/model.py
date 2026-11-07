from lematizador_regex.lematizador_regex import tokenizadoregex
import time
import numpy as np
from sklearn.nave_bayes import MultinomialNB


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
            if corpus[i] == pal_unico:
                matriz_bow[i][j] += matriz_bow[i][j] + 1
            j += 1
    return matriz_bow

#==================================================================
documentos = ["doc1.txt", "doc2.txt", "doc3.txt"]

for archivo in documentos:
    doctokenizado = tokenizadoregex(archivo)
    print("TEXTO TOKENIZADO:", doctokenizado)
    corpus += doctokenizado

corpus_prueba = corpus
print("CORPUS PRUEBA:", corpus_prueba)

vector_unico = eliminador_palabras_repetidas(corpus_prueba)
print("VECTOR UNICO:", vector_unico)

X = matriz_bag_words(corpus_prueba, vector_unico)
print("MATRIZ BAG OF WORDS:", X)

#Vector de etiquetas

y = [0, 1, 2, 3, 4]  # Etiquetas para cada documento



