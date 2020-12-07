import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
import sys
import tensorflow as tf

import config

def get_data():
	'''Essa função é responsável por pegar cada uma das imagens e ler como uma matriz de pixels. A matriz é dividida por 255 para que todos os valores dos pixels fiquem de 0 a 1. Ao final, a função retorna uma tupla em que os elementos são uma lista de matrizes de pixels e um lista de labels equivalentes para cada imagem
	'''
	images = []
	labels = []
	dir_path = os.path.join('datasets', 'original')
	for dir in os.listdir(dir_path):
		dir2_path = os.path.join(dir_path, dir)
		for dir2 in os.listdir(dir2_path):
			files_path = os.path.join(dir2_path, dir2)
			for file in os.listdir(files_path):
				image_path = os.path.join(files_path, file)
				img = cv2.imread(image_path, 1)
				img = cv2.resize(img, (config.IM_WIDTH, config.IM_HEIGHT))
				data = np.asarray(img)
				data = data/255.0
				label = file[-5:-4]
				images.append(data)
				labels.append(label)
	return (images, labels)

def main():

	images, labels = get_data()

	# Usa o sklearn para fazer a divisão dos dados em validação e treino
	labels = tf.keras.utils.to_categorical(labels)
	x_train, x_test, y_train, y_test = train_test_split(
		np.array(images), np.array(labels), test_size=config.TEST
	)
	
	# Define a rede neural compilada
	model = get_model()
	
	# Treina o modelo com os dados
	model.fit(x_train, y_train, epochs=config.EPOCHS)

	# Avalia a eficácia do modelo
	model.evaluate(x_test,  y_test, verbose=2)
	
	# Salva o modelo
	if len(sys.argv) == 2:
		filename = sys.argv[1]
		model.save(filename)
		print(f"Modelo {filename} salvo.")
	
def get_model():
	"""
	Retorna um modelo de rede neural sequencial usando TensorFlow e Keras
	"""
	model = tf.keras.Sequential([
		tf.keras.layers.Conv2D(32, 3, activation='relu', input_shape=(config.IM_WIDTH, config.IM_HEIGHT, 3)),
		tf.keras.layers.AveragePooling2D(pool_size=3),
		tf.keras.layers.Flatten(),
		tf.keras.layers.Dense(128, activation='relu'),
		tf.keras.layers.Dense(255, activation='relu'),
		tf.keras.layers.Dropout(0.5),
		tf.keras.layers.Dense(2, activation='softmax')
	])
	model.compile(
		optimizer='adam',
		loss='categorical_crossentropy',
		metrics=['accuracy']
	)
	return model	

if __name__ == "__main__":
	main()