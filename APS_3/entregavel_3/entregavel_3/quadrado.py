import rclpy
from rclpy.node import Node
import numpy as np
from my_package.odom import Odom
from geometry_msgs.msg import Twist

from math import *

class Quadrado(Node,Odom):
    def __init__(self):
        Node.__init__(self,'quadrado_node')
        Odom.__init__(self)
        self.timer = self.create_timer(0.25, self.control)


        # Inicialização de variáveis
        self.robot_state = 'andar'
        self.goal_yaw = 0
        self.time = self.get_clock().now().to_msg().sec
        self.twist = Twist()
        self.v = 0.25  # [m/s]
        self.states_machine = {
            'andar': self.andar,
            'girar': self.girar
        }
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)

    def control(self):
        self.twist = Twist()
        print(f'Estado Atual: {self.robot_state}')
        self.states_machine[self.robot_state]()

        self.cmd_vel_pub.publish(self.twist)

    # Utiliza a odometria para girar em 90 graus
    def girar(self):
        dif_360 = (self.goal_yaw - self.yaw_2pi ) % (2*pi)
        self.twist.angular.z = self.v
        print(dif_360)

        if dif_360 < np.deg2rad(2):
            self.time = self.get_clock().now().to_msg().sec
            self.robot_state = 'andar' 
            self.states_machine[self.robot_state]()

    def andar(self):
        self.twist.linear.x = self.v
        time_andando = self.get_clock().now().to_msg().sec
        dif_time =time_andando -  self.time
        self.t = dif_time
        print(self.t)

        if dif_time > 2.0:
            self.goal_yaw = (self.yaw_2pi + np.pi / 2) % (2 * np.pi)
            self.robot_state = 'girar' 
            self.states_machine[self.robot_state]()
def main(args=None):
    rclpy.init(args=args)
    ros_node = Quadrado()

    rclpy.spin(ros_node)

    ros_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
