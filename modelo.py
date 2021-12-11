import tensorflow as tf
import pandas as pd
import numpy as np


class model():
    def __init__(self):
        #Importar el archivo csv
        archivo = pd.read_csv("predicciones.csv", sep=";")
        tX = archivo.iloc[:,0:4].values
        pY = archivo.iloc[:,4:8].values
        prediccion = np.array([[21,23,40,40]])

        self.modelo = self.crearmodelo()
        self.modelo = self.compilar_entrenar(tX, pY)
        self.prediccion = self.predecir(prediccion)

    def crearmodelo(self):
        #Crear el modelo
        modelo = tf.keras.Sequential()
        #Crear una capa de entrada
        # modelo.add(tf.keras.layers.Sparc)
        modelo.add(tf.keras.layers.Dense(units=4, input_dim=4, activation='relu'))
        #Crear una capa de salida
        modelo.add(tf.keras.layers.Dense(units=4, activation='sigmoid'))

        return modelo

    def compilar_entrenar(self, modelo, tX, pY):
        #Compilar el modelo
        self.modelo.compile(optimizer='adam', loss='mean_squared_error', metrics=['binary_accuracy'])
        #Entrenar el modelo
        self.modelo.fit(tX, pY, epochs=100)

        return modelo

    def predecir(self, prediccion):
        #Predecir el resultado
        prediccion = self.modelo.predict(prediccion)
        real = np.argmax(prediccion)
        print(real)