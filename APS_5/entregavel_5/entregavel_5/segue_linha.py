import rclpy
from rclpy.node import Node
from rclpy.qos import ReliabilityPolicy, QoSProfile
from geometry_msgs.msg import Twist

import numpy as np
from math import *
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge

import cv2


# Adicione aqui os imports necessários



class SegueLinha(Node):
    def __init__(self):
        super().__init__('seguidor_node')
        self.posicao_x =0
        self.cX =0.0
        self.x_local = 0.0
        self.bridge = CvBridge()
        self.subscription = self.create_subscription(
            CompressedImage,
            'image_raw/compressed',
            self.image_callback,
            QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT))
    
        self.robot_state = 'segue'

        self.states_machine = {
            'centraliza': self.centraliza,
            'segue': self.segue,
            'erro' : self.erro
        }
        self.timer = self.create_timer(0.5, self.control)
        self.twist = Twist()
        self.offset = 30
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)    

    def filtro(self, cv_image):
           


            lower = (13, 121, 255)
            upper = (180,255,255) 
            result = cv2.inRange(cv_image, lower, upper)
            largura, altura = result.shape
            result[:int(largura/2),:] = 0
            #Parte da morfologia
            # Definição do kernel
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))


            # Operações Morfológicas

            # realiza a abertura
            mask = cv2.morphologyEx(result, cv2.MORPH_OPEN, kernel)
            mask = cv2.morphologyEx(result, cv2.MORPH_CLOSE, kernel)
            cv2.imshow('Mask',mask)



            # Realizando marcação de contorno
            contornos, arvore = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) 
            maior = None
            maior_area = 0
            if len(contornos) == 0:  # Verifica se a lista de contornos está vazia
                return 0, 0, 0, cv_image
            else:
            

            ## Utilizando max e key
                maior = max(contornos, key=cv2.contourArea)

            contornos_img = cv_image.copy()
            cv2.drawContours(contornos_img, [maior], -1, [255, 0, 0], 3)

            #Centro
            # Calcular o retângulo delimitador ao redor do maior contorno
            x, y, w, h = cv2.boundingRect(maior)

            # Desenhar o retângulo delimitador na imagem original
            cv2.rectangle(contornos_img, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Calcular o centro de massa do maior contorno
            M = cv2.moments(maior)
            if M["m00"] != 0:  # Verifica se o denominador não é zero
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            else:
                # Trate o caso em que o denominador é zero, por exemplo, definindo cX e cY como algum valor padrão
                cX = 0
                cY = 0

            # Desenhar um ponto no centro de massa na imagem original
            contornos_img = cv2.circle(contornos_img, (cX, cY), 2, (255, 0, 0), -1)
 
            
            return cX,cY,w,contornos_img
    
        

    #Rodando parte da movimentação

    
        # Inicialização de variáveis
    
    
    # Subscribers
    ## Coloque aqui os subscribers

    # Publishers
    ## Coloque aqui os publishers
    

    def centraliza(self):
        self.twist.linear.x= 0.0

        print(f'poscX {self.cX}')
        print(f'poslocal {self.x_local}')


        print(f'posX {self.posicao_x}')

        

        if self.cX > self.x_local + self.offset:
            self.twist.angular.z = -0.1
            print('entrou')
        
        elif self.cX < self.x_local - self.offset:
            self.twist.angular.z = 0.1

        else:
            self.robot_state = 'segue' 
    
            print('naosei')

        
    def segue(self):
        print(self.twist.linear.x)
        self.twist.angular.z = 0.0

        self.twist.linear.x= 0.1

        if self.cX == 0:
            self.robot_state = 'erro' 

        self.posicao_x = abs(self.cX - self.x_local)

        print('baom')
        if self.posicao_x > self.offset :
            self.maior = self.posicao_x
            self.menor =0
            self.robot_state = 'centraliza' 
            print( f'maior {self.maior}')


        else:
            print('baom3')




    def erro(self):
        if self.cX == None:
            self.twist.angular.z = 0.1
        else:
            self.robot_state = 'segue'

    def control(self):
        self.twist = Twist()
        self.states_machine[self.robot_state]()
        self.cmd_vel_pub.publish(self.twist)
        self.posicao_x = self.cX - self.x_local
        

        print('running...')

    def image_callback(self, msg):
        cv_image = self.bridge.compressed_imgmsg_to_cv2(msg, "bgr8")
        self.cX,self.cY,self.w,self.contornos_img = self.filtro(cv_image)
        

        self.x_local = cv_image.shape[0]/2
        self.y_local = cv_image.shape[1]/2

        cv2.imshow('Image',self.contornos_img)
        cv2.waitKey(1)


def main(args=None):
    rclpy.init(args=args)
    ros_node = SegueLinha() 
    rclpy.spin(ros_node) # tempo de execução do código

    ros_node.destroy_node() # resest os status
    rclpy.shutdown() #desliga


if __name__ == '__main__':
    main()
