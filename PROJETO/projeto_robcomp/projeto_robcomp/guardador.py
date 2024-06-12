import rclpy
from rclpy.node import Node
from rclpy.qos import ReliabilityPolicy, QoSProfile
from geometry_msgs.msg import Twist
from projeto_robcomp.derrubador import Derrubador
# Adicione aqui os imports necessários
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

class Guardador(Derrubador): # Mude o nome da classe

    def __init__(self , creepers_desejado , creepers_encontrados):

        Node.__init__(self , 'guardador_node') # Mude o nome do nó
        Derrubador.__init__(self , creepers_desejado , creepers_encontrados)

        self.drop_sub = self.create_subscription(
            String, 
            '/drop_area',
            self.drop_callback,
            10
        )
        self.timer = self.create_timer(0.1, self.control)

        self.robot_state = 'segue_linha'
        self.state_machine = {
            'stop': self.stop,
            'segue_linha' : self.segue_linha,
            'center': self.center,
            'center2': self.center2,
            'goto' : self.goto,
            'aproxima': self.aproxima, 
            'segura': self.segura 
        }

        # Inicialização de variáveis
        self.twist = Twist()
        
        # Subscribers
        ## Coloque aqui os subscribers

        # Publishers
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        ## Coloque aqui os publishers

    def drop_callback(self , msg):
        pass


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
            self.robot_state = 'stop'
            
    def segura(self):
        pass
    def stop(self):
        self.twist = Twist()

    def control(self):
        
        self.twist = Twist()
        print(f'Estado Atual: {self.robot_state}')
        self.state_machine[self.robot_state]()

        self.cmd_vel_pub.publish(self.twist)
        
            
def main(args=None):
    rclpy.init(args=args)
    
    
    
    
    dict_creepers = {'azul_11': [0.6481167095257608, -0.35660146258585634, 3.130151475406489], 'azul_21': [0.5085573604232402, -0.6204915158277664, 1.538924442243566], 'verde_32': [-1.5635097197769827, 1.3092279504640971, 3.7342596414295692], 'verde_13': [-1.672928535012047, -1.7037406358912623, 5.919186415557948]}

    ros_node = Guardador({'id' : 11 , 'cor' : 'azul'} , dict_creepers)
 
    rclpy.spin(ros_node)

    ros_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()