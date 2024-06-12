import rclpy
from rclpy.node import Node
from rclpy.qos import ReliabilityPolicy, QoSProfile
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Point
from std_msgs.msg import String
import cv2
import numpy as np
# Adicione aqui os imports necessários

class FiltroCor(Node): # Mude o nome da classe

    def __init__(self):
        super().__init__('filtro_cor_node') # Mude o nome do nó
        self.creeper_pos_pub = self.create_publisher(Point, '/creeper_position', 10)

        self.runnable = True


        # Inicialização de variáveis
        
        # Subscribers
        ## Coloque aqui os subscribers
        self.bridge = CvBridge()
        self.image_sub = self.create_subscription(
            CompressedImage, # or CompressedImage
            '/image_raw/compressed', # or '/camera/image_raw/compressed'
            self.image_callback,
            QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT))
        
        self.flag_sub = self.create_subscription(
            String,
            '/vision/image_flag', # Mude o nome do tópico
            self.flag_callback,
            QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT))

        # Publishers
        ## Coloque aqui os publishers

        
    def flag_callback(self, msg):
        self.runnable = bool(msg.data)

    def image_callback(self, msg):
            cv_image = self.bridge.compressed_imgmsg_to_cv2(msg, "bgr8")
            self.cX_azul,self.cY_azul,self.w_azul,self.contornos_img_azul,self.mask_azul = self.filtro_azul(cv_image)
            self.cX_verde,self.cY_verde,self.w_verde,self.contornos_img_verde,self.mask_verde = self.filtro_verde(cv_image)
            
            self.X,self.Y,self.Z,self.combinacao_contornos = self.combina(cv_image)

            self.x_local = cv_image.shape[1]/2
            self.y_local = cv_image.shape[0]/2            


            self.cX = self.X
            self.cY = self.Y




            cv2.imshow('Image Azul',self.mask_azul)
            cv2.imshow('Image Verde',self.mask_verde)
            cv2.imshow('Image Combina',self.combinacao_contornos)


            cv2.waitKey(1)        
            # Publicar a posição do creeper na imagem
            creeper_point = Point()
            creeper_point.x = float(self.cX)
            creeper_point.y = float(self.cY)
            creeper_point.z = float(cv_image.shape[1])  




            self.creeper_pos_pub.publish(creeper_point)
            

            print( float(self.cX))


    def filtro_verde(self, cv_image):

        # Definir os intervalos de cor verde em formato BGR
        lower_verde = (10, 20, 10)   # Matiz mínima, Saturação mínima, Valor mínima
        upper_verde = (80, 60, 40)

        # Aplicar a máscara para detectar a cor verde na imagem
        result_verde = cv2.inRange(cv_image, lower_verde, upper_verde)            
        largura, altura = result_verde.shape
        result_verde[:int(largura/2),:] = 0
        # Parte da morfologia
        # Definição do kernel
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

        # Operações Morfológicas Verde
        # Realizar abertura e fechamento para suavizar a máscara
        mask_verde = cv2.morphologyEx(result_verde, cv2.MORPH_OPEN, kernel)
        mask_verde = cv2.morphologyEx(result_verde, cv2.MORPH_CLOSE, kernel)

        # Realizando marcação de contorno
        contornos_verde, arvore = cv2.findContours(mask_verde.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) 
        maior_verde = None
        if len(contornos_verde) == 0:  # Verificar se a lista de contornos está vazia
            return 0, 0, 0, cv_image, mask_verde
        else:
            # Encontrar o maior contorno
            maior_verde = max(contornos_verde, key=cv2.contourArea)

        # Desenhar contornos na imagem original
        contornos_img_verde = cv_image.copy()
        cv2.drawContours(contornos_img_verde, [maior_verde], -1, [0, 255, 0], 3)

        # Calcular o retângulo delimitador ao redor do maior contorno
        x, y, w, h = cv2.boundingRect(maior_verde)

        # Desenhar o retângulo delimitador na imagem original
        cv2.rectangle(contornos_img_verde, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Calcular o centro de massa do maior contorno
        M = cv2.moments(maior_verde)
        if M["m00"] != 0:  # Verificar se o denominador não é zero
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            # Tratar o caso em que o denominador é zero
            cX = 0
            cY = 0

        # Desenhar um ponto no centro de massa na imagem original
        contornos_img_verde = cv2.circle(contornos_img_verde, (cX, cY), 2, (0, 255, 0), -1)

        return cX, cY, w, contornos_img_verde, mask_verde

    
    def filtro_azul(self, cv_image):
           

            lower_azul = (20, 30, 10)   # Matiz mínima, Saturação mínima, Valor mínima
            upper_azul = (90, 50, 50)
            result_azul = cv2.inRange(cv_image, lower_azul, upper_azul)            

            #Parte da morfologia
            # Definição do kernel
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))


            # Operações Morfológicas Verde

            # realiza a abertura
            mask_azul = cv2.morphologyEx(result_azul, cv2.MORPH_OPEN, kernel)
            mask_azul = cv2.morphologyEx(result_azul, cv2.MORPH_CLOSE, kernel)


            # Realizando marcação de contorno
            contornos_azul, arvore = cv2.findContours(mask_azul.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) 
            maior_azul = None
            if len(contornos_azul) == 0:  # Verifica se a lista de contornos está vazia
                return 0, 0, 0, cv_image,mask_azul
            else:

                ## Utilizando max e key
                maior_azul = max(contornos_azul, key=cv2.contourArea)

            contornos_img_azul = cv_image.copy()
            cv2.drawContours(contornos_img_azul, [maior_azul], -1, [255, 0, 0], 3)

            #Centro
            # Calcular o retângulo delimitador ao redor do maior contorno
            x, y, w, h = cv2.boundingRect(maior_azul)

            # Desenhar o retângulo delimitador na imagem original
            cv2.rectangle(contornos_img_azul, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Calcular o centro de massa do maior contorno
            M = cv2.moments(maior_azul)
            if M["m00"] != 0:  # Verifica se o denominador não é zero
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            else:
                # Trate o caso em que o denominador é zero, por exemplo, definindo cX e cY como algum valor padrão
                cX = 0
                cY = 0

            # Desenhar um ponto no centro de massa na imagem original
            contornos_img_azul = cv2.circle(contornos_img_azul, (cX, cY), 2, (0, 255, 0), -1)
            
            
            return cX,cY,w,contornos_img_azul,mask_azul
    
    def combina(self,cv_image):
        resultado = cv2.bitwise_or(self.mask_azul,self.mask_verde)
        # Realizando marcação de contorno
        contornos_azul, arvore = cv2.findContours(resultado.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) 
        maior_azul = None
        if len(contornos_azul) == 0:  # Verifica se a lista de contornos está vazia
            return 0, 0, 0, cv_image
        else:

            ## Utilizando max e key
            maior_azul = max(contornos_azul, key=cv2.contourArea)

        contornos_img_azul = cv_image.copy()
        cv2.drawContours(contornos_img_azul, [maior_azul], -1, [255, 0, 0], 3)

        #Centro
        # Calcular o retângulo delimitador ao redor do maior contorno
        x, y, w, h = cv2.boundingRect(maior_azul)

        # Desenhar o retângulo delimitador na imagem original
        cv2.rectangle(contornos_img_azul, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Calcular o centro de massa do maior contorno
        M = cv2.moments(maior_azul)
        if M["m00"] != 0:  # Verifica se o denominador não é zero
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            # Trate o caso em que o denominador é zero, por exemplo, definindo cX e cY como algum valor padrão
            cX = 0
            cY = 0

        # Desenhar um ponto no centro de massa na imagem original
        contornos_img_azul = cv2.circle(contornos_img_azul, (cX, cY), 2, (0, 255, 0), -1)
        
            
        return cX,cY,w,contornos_img_azul

            
def main(args=None):
    rclpy.init(args=args)
    ros_node = FiltroCor() # Mude o nome da classe

    rclpy.spin(ros_node)

    ros_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
