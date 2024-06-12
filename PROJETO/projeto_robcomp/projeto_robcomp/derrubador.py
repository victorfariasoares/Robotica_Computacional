import rclpy
from rclpy.node import Node
from rclpy.qos import ReliabilityPolicy, QoSProfile
from geometry_msgs.msg import Twist
from projeto_robcomp.reconhecedor import Reconhecedor
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
from my_package.laser import Laser
from numpy import sqrt
import random
# Adicione aqui os imports necessários

class Derrubador(Reconhecedor , Laser): # Mude o nome da classe

    def __init__(self , creeper_desejado , creepers_encontrados):
        Node.__init__(self , 'derrubador_node')
        Reconhecedor.__init__(self)
        Laser.__init__(self)

        time.sleep(2)

        self.timer = self.create_timer(0.25, self.control)

        self.robot_state = 'segue_linha'
        self.state_machine = {
            'stop': self.stop, 
            'segue_linha': self.segue_linha,
            'center': self.center,
            'goto': self.goto,
            'center2': self.center2,
            'aproxima': self.aproxima,
            'atropelador': self.atropelador
        }
        
        # Inicialização de variáveis
        self.coordenadas_creepers = creepers_encontrados
        self.nome_creepers = creeper_desejado
        orientacao_momento = self.coordenadas_creepers[self.nome_creepers][2]
        self.x_visto = self.coordenadas_creepers[self.nome_creepers][0]
        self.y_visto = self.coordenadas_creepers[self.nome_creepers][1]
        if orientacao_momento > 3 and orientacao_momento < 4:
            self.x_visto -= 0.2
        elif orientacao_momento > 1 and orientacao_momento < 2: 
            self.y_visto += 0.2
        elif orientacao_momento > 5:
            self.x_visto += 0.2
        self.kp_angular = 0.5
        self.kp_angular2 = 0.003
        self.kp_linear = 0.2
        self.derrubador = True
        self.point = (self.x_visto , self.y_visto)
        self.y0 = -0.36       
        self.twist = Twist()
        self.aruco_name = 0
        # Subscribers
        ## Coloque aqui os subscribers

        # Publishers
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        ## Coloque aqui os publishers
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
                self.cor = self.creeper['color']
                self.associa_creeper()
                if self.creeper_name == self.nome_creepers:
                    self.tem_creeper = True


    def get_error(self):
        
        if self.tem_creeper:
            self.ang_erro2 = self.cx_creeper - self.w
        else:
            self.ang_erro2 = -10

    def calcula_dist(self):
        self.dist = (self.x - self.x_visto) ** 2 + (self.y - self.y_visto) ** 2

    def segue_linha(self):
        
        if self.cx == -1:
            self.twist.angular.z = -0.6
            self.twist.linear.x = 0.
        else: 
            self.calcula_erro()
            self.twist.linear.x = 0.2
            self.twist.angular.z = self.erro * self.kp_ang1
            self.calcula_dist()
            if self.derrubador == True:
                if abs(self.y - self.y_visto) < 0.1 and self.dist < 1:
                    self.robot_state = 'center'
            else:
                if abs(self.y0 - self.y) < 0.05:
                    self.point = (2.91 , -0.35)
                    self.robot_state = 'center'
            

    def center(self):
        
        self.get_angular_erro(self.point)
        self.twist.angular.z = self.kp_angular * self.erro_ang
        print(abs(self.erro_ang))
        if abs(self.erro_ang) < 0.1:
            self.robot_state = 'goto'

    def center2(self):
        self.get_error()
        
        if not(self.tem_creeper):
            #self.twist.linear.x = 1e-2
            self.twist.angular.z = 0.15
        else:
            self.twist.linear.x = 0.
            
            self.twist.angular.z = self.kp_angular2 * -self.ang_erro2
            
            print('Velocidade em z é : ' , self.twist.angular.z)
            print('O Erro angular é :' , abs(self.ang_erro2))
            print('O Centro do Aruco é: ' , self.cx_creeper)
            print('O Centro da Camera é: ' , self.cx)
            if abs(self.ang_erro2) < 0.05:
                self.twist.angular.z = 0.
                self.robot_state = 'aproxima'
                
    def aproxima(self):
        
        self.get_error()
        if self.tem_creeper:
            self.twist.angular.z = self.kp_angular2 * -self.ang_erro2
            self.twist.linear.x = min(self.front) * self.kp_linear
        else:
            self.twist.angular.z = 0.
            self.twist.linear.x = 0.05

        print(min(self.front))
        
        if min(self.front) < 0.2:
            self.twist.linear.x = 0.
            self.robot_state = 'atropelador'
    
    def atropelador(self):

        self.twist.linear.x = 0.05

        if min(self.front) > 0.2:
            self.twist.linear.x = 0.
            self.robot_state = 'segue_linha'
            self.derrubador = False

    def goto(self):
        
        self.get_angular_erro(self.point)
        
        print('X é :' , self.x)
        print('Y é :' , self.y)
        print('O theta é :' , self.theta )
        print('Yaw é :' , self.yaw)
        print('O erro é :' , self.erro_ang)
        
        self.twist.angular.z = self.kp_angular * self.erro_ang
        self.twist.linear.x = self.kp_linear * self.dist
        if self.dist < 0.05 and self.derrubador:
            self.twist.linear.x = 0.
            self.robot_state = 'center2'
        elif self.derrubador == False and self.dist < 0.05:
            self.twist.linear.x = 0.
            self.robot_state = 'stop'
    

    def control(self):
        self.twist = Twist()
        print(f'Estado Atual: {self.robot_state}')
        self.state_machine[self.robot_state]()
        print('Tem Creeper? ' , self.tem_creeper)
        print('Derrubador Roda?' , self.derrubador)
        print('O ponto desejado é :' , self.point)
        self.cmd_vel_pub.publish(self.twist)
        print('O creeper desejado é: ' , self.nome_creepers)
            
def main(args=None):
    rclpy.init(args=args)
    
    dict_creepers = {'azul_11': [0.6481167095257608, -0.35660146258585634, 3.130151475406489], 'azul_21': [0.5085573604232402, -0.6204915158277664, 1.538924442243566], 'verde_32': [-1.5635097197769827, 1.3092279504640971, 3.7342596414295692], 'verde_13': [-1.672928535012047, -1.7037406358912623, 5.919186415557948]}
    ids = [13 , 21 , 11 , 32]
    numero_sorteado = random.choice(ids)
    associacao = {13 : 'verde_13' , 11: 'azul_11' , 21: 'azul_21' , 32: 'verde_32' }

    ros_node = Derrubador(associacao[numero_sorteado] , dict_creepers) # Mude o nome da classe

    rclpy.spin(ros_node)

    ros_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()