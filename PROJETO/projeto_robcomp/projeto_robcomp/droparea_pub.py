import time
import rclpy
from rclpy.node import Node
from rclpy.qos import ReliabilityPolicy, QoSProfile
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import String
from cv_bridge import CvBridge
from my_package.atividade3 import DistanceEstimator
from my_package.qr_code_identifier import QRCODER
import cv2
import json
from std_msgs.msg import String
from my_package.box_detector import AnimalDetector
import numpy as np

class Creepers(Node , AnimalDetector): # Mude o nome da classe

    def __init__(self):
        Node.__init__(self, 'identifica_creepers_node') # Mude o nome do nó
        AnimalDetector.__init__(self)
        self.bridge = CvBridge()
        self.subcomp = self.create_subscription(
            CompressedImage,
            '/camera/image_raw/compressed',
            self.image_callback,
            QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE)
        )
        self.ranked_arucos = {}
        time.sleep(3)
        self.timer = self.create_timer(0.1, self.control)

        # Inicialização de variáveis
        self.results = []
        # Subscribers
        ## Coloque aqui os subscribers

        # Publishers
        self.animal_pub = self.create_publisher(String , 'drop_area' , 10)

    def image_callback(self, msg):
        
        cv_image = self.bridge.compressed_imgmsg_to_cv2(msg, "bgr8")
        bgr , self.dict_animals , self.results = self.encontra_animal(cv_image)
        
        cv2.imshow("Imagem", bgr)
        cv2.waitKey(1)
        

    def control(self):
        msg = String()
        msg.data = json.dumps([])
        if len(self.results) > 0: 
            msg.data = json.dumps(self.dict_animals)
            
        print(msg.data)
        self.animal_pub.publish(msg)
        
            
def main(args=None):
    rclpy.init(args=args)
    ros_node = Creepers() 

    rclpy.spin(ros_node)

    ros_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
