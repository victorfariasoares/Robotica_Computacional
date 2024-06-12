import time
import rclpy
from rclpy.node import Node
from rclpy.qos import ReliabilityPolicy, QoSProfile
from geometry_msgs.msg import Twist
# Adicione aqui os imports necessários
from sensor_msgs.msg import CompressedImage
import cv2
import numpy as np
import matplotlib.pyplot as plt
from cv_bridge import CvBridge
from std_msgs.msg import String
import json 
from nav_msgs.msg import Odometry
from my_package.odom import Odom
from numpy import sqrt
class Reconhecedor(Node , Odom): # Mude o nome da classe

    def __init__(self):
        # Subscribers e Herança
        Node.__init__(self , 'reconhecedor_node') # Mude o nome do nó
        Odom.__init__(self)

        self.qr_codes = []
        self.timer = self.create_timer(0.1, self.control)
        self.bridge = CvBridge()

        self.subcomp = self.create_subscription(
            CompressedImage,
            '/camera/image_raw/compressed',
            self.image_callback,
            QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE)
        )
        
        self.creeper_sub = self.create_subscription(
            String,
            '/creeper',
            self.creeper_callback,
            QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE)
        )

        self.aruco_sub = self.create_subscription(
            String,
            '/qr_code',
            self.aruco_callback,
            10
        )

        time.sleep(3)

        # Inicialização de variáveis
        self.twist = Twist()
        self.kp_ang1 = 0.007
        self.kp_angular = 0.2
        self.kp_linear = 0.2
        self.cx = -1
        self.cy = -1
        self.creepers = {}
        self.arucos = {}
        self.tem_aruco = False
        self.tem_creeper = False
        self.i = 0
        self.funcionando = False
        # Publishers
        self.twist = Twist()
        self.start = (2.91 , -0.35)
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)

        self.robot_state = 'segue_linha'
        self.state_machine = {
            'stop': self.stop,
            'segue_linha': self.segue_linha,
            'center': self.center,
            'goto': self.goto,
            'stop': self.stop
        }
    

    def aruco_callback(self , msg2):
        self.qr_codes = json.loads(msg2.data)
        self.tem_aruco = False
        self.aruco_name = ""
        if len(self.qr_codes) > 0:
            self.ID_aruco = str(self.qr_codes[0]["id"][0])
            self.associa_aruco()
            self.tem_aruco = True
        
    def creeper_callback(self, msg):

        self.ranked_arucos = json.loads(msg.data)
        
        if bool(self.ranked_arucos):
            self.creeper = self.ranked_arucos
            self.ID = str(self.creeper["id"][0])
            self.distancia = self.creeper["distancia"]
            self.centro_corpo = self.creeper["body_center"]
            self.cx_creeper = self.centro_corpo[0]
            self.cy_creeper = self.centro_corpo[1]
            self.tem_creeper = False
            if float(self.ID) < 100:
                self.tem_creeper = True
                self.cor = self.creeper['color']
                self.associa_creeper()
            
    def image_callback(self , msg):

        self.cv_image = self.bridge.compressed_imgmsg_to_cv2(msg, "bgr8")
        copia_camera = self.cv_image.copy()

        self.mascara_camera = self.faz_mascara(copia_camera)
        self.imagem_redefinida = self.redefine_dimensão(copia_camera)

        self.h , self.w , _ = self.cv_image.shape        
        self.w = self.w/2

        self.mascara_camera[:int(self.h/2),:] = 0

        self.acha_cm()
        cv2.imshow('Image', self.cv_image)
        cv2.imshow('Image_Reduced' , self.imagem_redefinida)
        cv2.imshow('Mask_Camera' , self.mascara_camera)
        cv2.waitKey(1)

    def associa_aruco(self):
        
        self.aruco_name += self.ID_aruco 

        if self.aruco_name not in self.arucos.keys():
            self.arucos[self.aruco_name] = self.qr_codes

    def associa_creeper(self):
        self.creeper_name = ""
        if self.cor == 'green':
            self.creeper_name += 'verde_'
        else:
            self.creeper_name += 'azul_'
        self.creeper_name += self.ID

        if self.creeper_name not in self.creepers.keys():
            self.creepers[self.creeper_name] = [self.x , self.y , self.yaw_2pi]
        
    def faz_mascara(self , imagem): 
        
        img_copy = cv2.cvtColor(imagem , cv2.COLOR_BGR2HSV)

        kernel = np.ones((10,10), np.uint8)

        limite_inferior = np.array([15, 110, 170])
        limite_superior = np.array([35, 255, 255])

        mascara = cv2.inRange(img_copy , limite_inferior , limite_superior)
        mascara = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel)
        mascara = cv2.morphologyEx(mascara, cv2.MORPH_CLOSE, kernel)
        

        return mascara
    
    def redefine_dimensão(self , imagem):
        height = self.cv_image.shape[0]
        imagem[:int(height/2)] = 0
        
        return imagem

    def acha_cm(self):

        contours, _ = cv2.findContours(self.mascara_camera, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) > 0:
            contour = max(contours, key=cv2.contourArea)
            cv2.drawContours(self.cv_image, contour, -1, [255, 0, 0], 3)

            M = cv2.moments(contour)
            self.cx = int(M["m10"] / M["m00"])
            self.cy = int(M["m01"] / M["m00"])
            cv2.circle(self.cv_image, (self.cx, self.cy), 5, (0, 0, 255), -1)
        else:
            self.cx = -1
            self.cy = -1



    def calcula_erro(self):

        self.erro = self.w - self.cx
        
        
    def segue_linha(self): 
        
        if self.cx == -1:
            self.twist.angular.z = -0.6
            self.twist.linear.x = 0.
        else: 
            self.calcula_erro()
            self.twist.linear.x = 0.2
            self.twist.angular.z = self.erro * self.kp_ang1
            if len(self.creepers) == 4 and abs(self.y - self.start[1]) <= 0.05:
                self.robot_state = 'center'
        
    def get_angular_erro(self , point):

        #Calculo da distancia 

        self.err_x = point[0] - self.x
        self.err_y = point[1] - self.y
        self.dist = sqrt(self.err_x ** 2 + self.err_y ** 2)


        #Calculo do Angulo Desejado 

        self.theta = np.arctan2(point[1]-self.y , point[0]-self.x)
        self.erro_ang = self.theta - self.yaw
        self.erro_ang = np.arctan2(np.sin(self.erro_ang), np.cos(self.erro_ang))

    def center(self):

        self.get_angular_erro(self.start)
        self.twist.angular.z = self.kp_angular * self.erro_ang
        print(abs(self.erro_ang))
        if abs(self.erro_ang) < 0.1:
            self.robot_state = 'goto'
    
    def goto(self):
        
        self.get_angular_erro(self.start)
        
        print('X é :' , self.x)
        print('Y é :' , self.y)
        print('O theta é :' , self.theta )
        print('Yaw é :' , self.yaw)
        print('O erro é :' , self.erro_ang)
        
        self.twist.angular.z = self.kp_angular * self.erro_ang
        self.twist.linear.x = self.kp_linear * self.dist
        if self.dist < 0.05:
            self.robot_state = 'stop'
            
    def stop(self):
        self.twist = Twist()
        



    def control(self):
        print(self.creepers)
        print('Tem Aruco?' , self.tem_aruco)
        self.twist = Twist()
        print(f'Estado Atual: {self.robot_state}')
        self.state_machine[self.robot_state]()
        self.i += 1 
        self.cmd_vel_pub.publish(self.twist)
        print(len(self.qr_codes))
        print('O ponto é : ' , self.start)
def main(args=None):
    rclpy.init(args=args)
    ros_node = Reconhecedor() # Mude o nome da classe

    rclpy.spin(ros_node)

    ros_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()