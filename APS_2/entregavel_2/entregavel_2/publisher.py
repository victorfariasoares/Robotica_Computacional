import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from nav_msgs.msg import Odometry
from rclpy.qos import ReliabilityPolicy, QoSProfile
import numpy as np

"""
ros2 launch entregavel_2 publisher.launch.py
"""

class FirstNode(Node):

    def __init__(self):
        super().__init__('publisher')
        self.vel_pub = self.create_publisher(String, 'publisher', 10)

        self.timer = self.create_timer(1, self.control)
        self.contador = 0

    def control(self):
        self.contador +=1
        self.msg = String()
        tempo_sec = self.get_clock().now().to_msg().nanosec
        self.msg.data = f'{tempo_sec} {self.contador}'
        print(f'Olá, são {tempo_sec} e estou publicando pela {self.contador} vez')
        self.vel_pub.publish(self.msg)


def main(args=None):
    rclpy.init(args=args)
    publisher = FirstNode()

    rclpy.spin(publisher)

    publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
