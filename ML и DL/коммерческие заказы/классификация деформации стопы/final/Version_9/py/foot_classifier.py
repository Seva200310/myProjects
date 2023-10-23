from keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import pandas as pd
import cv2
import matplotlib.pyplot as plt
import base64
import os

class Foot_classifier():
    def __init__(self):
        self.model_seg = load_model('model_segmentation.h5')
        self.model_left= load_model('model_classification_left.h5')
        self.model_right= load_model('model_classification_right.h5')
        dummies=list(pd.get_dummies(['0L', '0R', '1L', '1R', '2L', '2R', '3L', '3R','NL','NR']).values)
        self.dictionary=dict(zip(['0L', '0R', '1L', '1R', '2L', '2R', '3L', '3R','NL','NR'],dummies))
        self.classes=['0L', '0R', '1L', '1R', '2L', '2R', '3L', '3R','NL','NR']
    def readb64(self,uri):
        #print(uri)
        encoded_data = uri.split(',')[1]
        nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img
    def prepare_image(self,photo,new_shape=(224,224)):
        x = self.readb64(photo)
        x = cv2.resize(x,new_shape)/255
        #x = load_img(photo, target_size=new_shape)
        #x = img_to_array(x) / 255.0  # Нормализация значений пикселей
        return x
    def save_image(self,img_with_mask,pred_vector_left,pred_vector_right,name):
        def_left=np.argmax(pred_vector_left)
        if def_left==4:
            def_left='-'
        def_right=np.argmax(pred_vector_right)
        if def_right==4:
            def_right='-'
        text=f'Левая:{def_left} \n Правая:{def_right}'
        fig, ax = plt.subplots(1)
        ax.imshow(img_with_mask)
        ax.text(8, 15, text, bbox={'facecolor': 'white', 'pad': 10})
        fig.savefig(name)
    def make_classification(self,photo,name):
        print('Инициализация пройдена')
        img=self.prepare_image(photo)
        filename=len(os.listdir('collectedData'))
        cv2.imwrite(f'collectedData/{filename}.png', img*255)
        print('Изображение готово')
        mask=self.model_seg.predict(np.array([img]))[0]
        pred_left=self.model_left.predict(np.array([mask]))[0]
        pred_right=self.model_right.predict(np.array([mask]))[0]
        print('предсказания сделаны')
        self.save_image(mask,pred_left,pred_right,name)
        print('Готово')
        return name
        



#classifier=Foot_classifier()
#classifier.make_classification('18.jpg','mask.png')
