import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from rclpy.qos import ReliabilityPolicy, QoSProfile

class Subscriber(Node):

    def __init__(self):
        super().__init__('subscriber')
        self.timer = self.create_timer(1, self.control)

        self.mensagem = 0

        self.odom_sub = self.create_subscription(
            String,
            '/publisher',
            self.odom_callback,
            QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE))

    def odom_callback(self, data: String):
        self.mensagem = data.data
        string_msg = self.mensagem.split()
        self.contador = string_msg[1]
        time = int(string_msg[0])
        self.df_time = (self.get_clock().now().to_msg().nanosec - time) / (10**9)
        

    def control(self):
        print(f'Contador: {self.contador}')
        print(f'Tempo Decorrido: {self.df_time}')
        
def main(args=None):
    rclpy.init(args=args)
    subscriber = Subscriber()

    rclpy.spin(subscriber)

    subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
