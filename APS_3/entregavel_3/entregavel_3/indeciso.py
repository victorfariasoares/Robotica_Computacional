import rclpy
from rclpy.node import Node
from rclpy.qos import ReliabilityPolicy, QoSProfile
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from my_package.laser import Laser
# Adicione aqui os imports necessários

class Indeciso(Node,Laser):

    def __init__(self):
        Node.__init__(self,'indeciso_node')
        Laser.__init__(self)
        self.timer = self.create_timer(1, self.control)
        #self.front = self.front  
        self.contador =0
        self.robot_state = 'forward'
        self.state_machine = {
            'stop': self.stop,
            'forward': self.forward,
            'backward': self.backward,
        }

        # Inicialização de variáveis
        self.twist = Twist()
        
       

        # Publishers
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        ## Coloque aqui os publishers

    def stop(self):
        self.twist.linear.x = 0.0

    def forward(self):
        self.twist.linear.x = 0.2
        front_distance = min(self.front)
        if front_distance >= 1.05:
            self.robot_state = 'forward'
        elif front_distance <= 0.95:
            self.robot_state = 'backward'


    def backward(self):
        self.twist.linear.x = -0.2 
        front_distance = min(self.front)
        print(self.contador)
        if self.contador > 2:
            self.robot_state = 'stop'
        
        elif front_distance >= 1.05:
            self.contador += 1
            self.robot_state = 'forward'

   

    def control(self):
        self.twist = Twist()

        print(f'Estado Atual: {self.robot_state}')
        self.state_machine[self.robot_state]()
        self.cmd_vel_pub.publish(self.twist)

        
            
def main(args=None):
    rclpy.init(args=args)
    ros_node = Indeciso() # Mude o nome da classe

    rclpy.spin(ros_node)

    ros_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
