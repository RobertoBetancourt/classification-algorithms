from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support

# Agregar los atributos en un vector
Archivo = open('string_to_word_vector.csv', 'r')
Clases = []
Valores = []
for x in Archivo.readlines():
  if len(x) > 1 and x[:5] != "class":
    Atrib = x.replace('\n', '').split(',')
    Clases.append(Atrib[0])
    Valores.append(list(map(float, Atrib[2:])))

# Separar conjunto de entrenamiento y de evaluación
Datos_train, Datos_test, Clase_Train, Clase_Test = train_test_split(Valores, Clases, test_size=0.2)

# Definir modelo (elegir clasificador)
algoritmo = KNeighborsClassifier(n_neighbors=1, metric='euclidean')

# Entrenamiento
algoritmo.fit(Datos_train, Clase_Train)

# Clasificar el test
ClasesRecuperadas = algoritmo.predict(Datos_test)

Matriz = confusion_matrix(Clase_Test, ClasesRecuperadas)
tn, fp, fn, tp = confusion_matrix(Clase_Test, ClasesRecuperadas).ravel()
print('Confusion matrix:')
print(Matriz)

precision, recall, fscore, _ = precision_recall_fscore_support(Clase_Test, ClasesRecuperadas, average='micro')
print('Precision: ', precision, '\nRecall: ', recall, '\nF-score', fscore)