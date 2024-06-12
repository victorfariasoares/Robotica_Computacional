import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist,Point
from my_package.laser import Laser
import numpy as np
from math import *

import cv2
# Adicione aqui os imports necessários

class Aproxima(Node,Laser): # Mude o nome da classe

    def __init__(self):
        Node.__init__(self, 'aproxima_node')
        Laser.__init__(self)

        self.timer = self.create_timer(0.25, self.control)
        self.posicao_x=0.0
        self.robot_state = 'centraliza'
        self.state_machine = {
            'segue': self.segue,
            'centraliza': self.centraliza,
            'stop': self.stop,
            'erro': self.erro
        }

        # Inicialização de variáveis
        self.twist = Twist()
        self.point = Point()

        self.timer = self.create_timer(0.5, self.control)
        self.offset = 30
        self.cX = 0.0
        self.cY= 0.0
        self.w = 0.0


        
        

        # Subscribers
        ## Coloque aqui os subscribers
        self.subscription = self.create_subscription(
            Point,
            '/creeper_position', # Mude aqui o topico
            self.creeper_callback,
            10)


        # Publishers
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        ## Coloque aqui os publishers
    
    def creeper_callback(self,msg):
        self.x_creeper = msg.x
        self.y_creeper = msg.y
        self.z_creeper = msg.z
        self.x_local = msg.z/2
        

    def stop(self):
        self.twist.linear.x = 0.0
        self.twist.angular.z = 0.0
        self.front_distance = min(self.front)
        print(self.front_distance)
        if (self.front_distance > 0.5 ):
            self.robot_state = 'centraliza' 



    def control(self):
        self.twist = Twist()
        print(f'Estado Atual: {self.robot_state}')
        self.state_machine[self.robot_state]()

        self.cmd_vel_pub.publish(self.twist)
        self.cX = self.x_creeper
        self.cY= self.y_creeper
        self.w = self.z_creeper

        
    def centraliza(self):
        self.twist.linear.x= 0.0
        self.twist.angular.z = 0.0

        print(f'poscX {self.cX}')
        print(f'poslocal {self.x_local}')


        print(f'posX {self.posicao_x}')

        
        
        if self.cX > self.x_local + self.offset:
            self.twist.angular.z = -0.1
            print('maior')
        

        elif self.cX < (self.x_local - self.offset):
            self.twist.angular.z = 0.1
            print('menor')

        else:
            self.robot_state = 'segue' 
    
            print('naosei')

        
    def segue(self):
        self.twist.angular.z = 0.0
        self.twist.linear.x= 0.1
        self.posicao_x = abs(self.cX - self.x_local)
        self.front_distance = min(self.front)
        if self.cX == 0:
            self.robot_state = 'erro' 
        elif (self.front_distance <= 0.5 ):
            self.robot_state = 'stop' 

        else:
            print('baom')
            if self.posicao_x > self.offset :
                self.maior = self.posicao_x
                self.menor =0
                self.robot_state = 'centraliza' 
                print( f'maior {self.maior}')





    def erro(self):
        self.twist.linear.x= 0.0

        if self.cX == 0:
            self.twist.angular.z = 0.1
            print(self.cX)
        else:
            self.robot_state = 'segue'
            
def main(args=None):
    rclpy.init(args=args)
    ros_node = Aproxima() # Mude o nome da classe
    

    rclpy.spin(ros_node)

    ros_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
