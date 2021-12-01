# Proyecto Final - Sistemas inteligentes

## preprocessing.py
Este programa se encarga de aplicar ciertos filtros para el preprocesamiento del texto, y genera un archivo en formato txt con las oraciones ya procesadas.

Se puede modificar el nombre de los archivos de entrada y salida, así como los filtros a aplicar, en a partir de la línea 118.

## file_converter.py
Programa que se recibe como entrada un archivo de texto, y genera un archivo en formato .arff, que puede ser leído por Weka.

El nombre de los archivos de entrada y salida se pueden modificar en la línea 72.

## naive-bayes.py
Este programa recibe como entrada redireccionada un archivo de texto, e imprime en consola la matriz de confusión, después de aplicar el algoritmo Naive Bayes con un split de 90/10.

## knn-algorithm.py
Recibe una lista de vectores en formato csv (el nombre del archivo puede ser modificado en la línea 6), e imprime en consola la matriz de confusión, después de aplicar el algoritmo de KNN.

## Varios archivos
reviews.txt consiste en el dataset original, mientras que reviews.arff en el fondo es el mismo archivo pero con la extensión y los tags adecuados para su lectura en Weka.

processed_text.txt es el output del archivo de preprocesamiento, con los filtros aplicados

model.csv es el archivo que genera el preprocesamiento de Weka, al aplicar la función de StringToWordVector