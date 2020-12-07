import cv2
import numpy as np
import os
import sys
import tensorflow as tf
import grad_cam
from rede import config

def predict(file):
	'''Carrega o modelo e faz a predição'''
	model = tf.keras.models.load_model(config.MODEL)
	layer_names=[layer.name for layer in model.layers]
		
	path = os.path.relpath(file)
	img = cv2.imread(path)
	
	data = pre_process_img(img)
	
	prediction = model.predict(data).tolist()
	
	normalize(prediction)
	show_img(img)
	
	guided_model = grad_cam.build_guided_model()
	gradcam, gb, guided_gradcam = grad_cam.compute_saliency(model, guided_model, layer_name=layer_names[0],
                                             img_path=path, cls=-1, visualize=True, save=True)
	return prediction
	
def pre_process_img(img):
	'''Escala a imagem para ficar compativel com o modelo'''
	img = cv2.resize(img, (config.IM_WIDTH, config.IM_HEIGHT))
	data = np.asarray(img)
	data = data/255.0
	data = np.expand_dims(data, 0)
	return data
	
def normalize(prediction):
	'''Normaliza a distribuição de probabilidade'''
	contador = 0
	for predict in prediction:
		for probs in predict:
			contador += probs
	for predict in prediction:
		for probs in predict:
			probs *= 1/contador

	tipo = ['Benigno', 'Maligno']
	tipo_pred = tipo[prediction[0].index(max(prediction[0]))]
	prob = max(prediction[0])*100
	print('\n \t Tipo de Câncer: {} \n \t Probabilidade: {:.3f}%'.format(tipo_pred, prob))
	
	################################
	font_scale = 1
	font = cv2.FONT_HERSHEY_PLAIN

	# set the rectangle background to white
	rectangle_bgr = (250, 238, 245)
	# make a black image
	window = np.zeros((500, 500))
	# set some text
	text = 'Tipo de Cancer: {},  Probabilidade: {:.3f}%'.format(tipo_pred, prob)
	# make the coords of the box with a small padding of two pixels
	box_coords = ((0, 0), (500, 500))
	cv2.rectangle(window, box_coords[0], box_coords[1], (250, 0, 0), cv2.FILLED)
	cv2.putText(window, text, (50, 250), font, fontScale=font_scale, color=(0, 0, 0), thickness=1)
	cv2.imshow("Resultado", window)
	cv2.waitKey(0)
	
	return
	
def show_img(img):
	'''Mostra a imagem antes'''
	img = cv2.resize(img, (300, 300))
	cv2.imshow('Histograma Original', img)
	cv2.waitKey(0)
	return