import cv2
import numpy as np
from math import *

class Atividade1():
    def __init__(self):
        # Definir aqui os atributos da classe
        self.ciano = {
            'lower': (85,100,100),
            'upper': (105,255,255)
        }

        self.magenta = {
            'lower': (125, 100, 100),
            'upper': (165, 255, 255)
        }

        self.f = 361.68 # Distância focal da câmera [px]
        self.H = 8.0  # Distancia real entre os circulos [cm]

    def encontrar_foco(self, D: float, h: float):
        """Não mude ou renomeie esta função
        Entradas:
        D - distancia real da câmera até o objeto [m]
        h - a distancia virtual entre os circulos [px]
        Saída:
        f - a distância focal da câmera [px]
        """
        f = D * h / self.H

        return f
    
    def encontrar_D(self, h: float):
        """Não mude ou renomeie esta função
        Entrada:
            f - a distância focal da câmera [px]
            h - a distancia virtual entre os circulos [px]
        Saída:
            D - distancia real da câmera até o objeto [m]
        """
        if h == 0:
            return -1
        D = ((self.H)*self.f)/h
        return D

    def run(self, bgr: np.ndarray):
        """Não mude ou renomeie esta função
        Entrada:
            bgr (np.ndarray): Frame de entrada

        Returns:
            bgr (np.ndarray): Frame com o exercicio 1 desenhado
            D (float): Distancia real da câmera até o objeto [m]
            h (float): a distancia virtual entre os circulos [px]
        """
        img_hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)

        #Mascara para ciano 

        mask_ciano = cv2.inRange(img_hsv.copy(), self.ciano['lower'], self.ciano['upper'])

        #Mascara para magenta
        mask_mag = cv2.inRange(img_hsv.copy(), self.magenta['lower'], self.magenta['upper'])

        #Calculando area ciano
        media = np.mean(mask_ciano)
        codicionado_ciano = mask_ciano.copy()
        codicionado_ciano[codicionado_ciano < media] = 0
        codicionado_ciano[codicionado_ciano >= media] = 255
        area_ciano = np.count_nonzero(codicionado_ciano)

        #Calculando area magenta
        media = np.mean(mask_mag)
        codicionado_mag = mask_mag.copy()
        codicionado_mag[codicionado_mag < media] = 0
        codicionado_mag[codicionado_mag >= media] = 255
        area_mag = np.count_nonzero(codicionado_mag)
        #Diferença das áreas
        if abs(area_ciano-area_mag) > 20000:
            D = -1
            h=0
        else:
            A = (area_ciano + area_mag)/2
            
            h = sqrt(4*A/pi)
            D = round(self.encontrar_D(h),2)
            
            
        texto = f'Diametro: {round(h,2)}, Distancia: {D}'
        
        bgr = cv2.putText(bgr, texto, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        return bgr, D


def rodar_frame():
    RodaAtividade = Atividade1()
    
    bgr = cv2.imread("img/q1/v.png") # Use esta imagem para calibrar a câmera
    # bgr = cv2.imread("img/q1/teste01.jpg") # Ditancia esperada: ~ 41 cm
    bgr, D = RodaAtividade.run(bgr)

    cv2.imshow("Imagem", bgr)
    cv2.waitKey(0)


def rodar_webcam():
    RodaAtividade = Atividade1()
    cap = cv2.VideoCapture(0)

    while True:
        ret, bgr = cap.read()
        bgr, D = RodaAtividade.run(bgr)

        cv2.imshow("Imagem", bgr)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
def main():
    # Selecione se deseja rodar seu codigo com uma imagem ou um video:
    # rodar_frame()
    rodar_webcam()


if __name__ == "__main__":
    main()