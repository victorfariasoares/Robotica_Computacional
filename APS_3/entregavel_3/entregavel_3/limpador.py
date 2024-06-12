import rclpy
from rclpy.node import Node
from rclpy.qos import ReliabilityPolicy, QoSProfile
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from my_package.laser import Laser
import numpy as np
from my_package.odom import Odom
from math import *
# Adicione aqui os imports necessários

class Limpador(Node,Laser,Odom): # Mude o nome da classe

    def __init__(self):
        Node.__init__(self,'limpador_node')# Mude o nome do nó
        Laser.__init__(self)
        Odom.__init__(self)
        self.timer = self.create_timer(0.5, self.control)
        self.robot_state = 'forward'

        self.states_machine = {
            'forward': self.forward,
            'turn': self.turn,

        }

        # Inicialização de variáveis
        self.twist = Twist()
        
        # Subscribers
        # ## Coloque aqui os subscribers
        # self.laser_sub = self.create_subscription(
        #     LaserScan,
        #     '/scan',
        #     self.laser_callback,
        #     QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT))

        # Publishers
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        ## Coloque aqui os publishers

   

    def forward(self):
        self.twist.linear.x = 0.2
        front_distance = min(self.front)
        if (front_distance <= 0.6 ):
            self.twist.linear.x= 0.0
            self.goal_yaw = (self.yaw_2pi + np.deg2rad(225)) % (2 * np.pi)
            print(f'self.goal_yaw : {np.rad2deg(self.goal_yaw)}')
            self.robot_state = 'turn' 
        
            
    def turn(self):
        # Utiliza a odometria para girar em 225 graus
        print(self.front[0:])
        self.dif_360 = abs((self.goal_yaw - self.yaw_2pi )) % ( 2 * pi)
        self.twist.angular.z = 0.5
        print(f'self.dif_360 : {np.rad2deg(self.dif_360)}')

        if self.dif_360 < np.deg2rad(10):
            self.robot_state = 'forward' 
            self.twist.angular.z = 0.0

    def control(self):
        self.twist = Twist()
        self.states_machine[self.robot_state]()
        self.cmd_vel_pub.publish(self.twist)

        
            
def main(args=None):
    rclpy.init(args=args)
    ros_node = Limpador() 
    rclpy.spin(ros_node)

    ros_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
