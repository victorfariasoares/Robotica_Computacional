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

import numpy as np

class Creepers(Node, DistanceEstimator , QRCODER): # Mude o nome da classe

    def __init__(self):
        Node.__init__(self, 'identifica_creepers_node') # Mude o nome do nó
        DistanceEstimator.__init__(self)
        QRCODER.__init__(self)

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
        
        # Subscribers
        ## Coloque aqui os subscribers

        # Publishers
        self.creeper_pub = self.create_publisher(String, 'creeper', 10)
        self.qrs_pub = self.create_publisher(String , 'qr_code' , 10)                                

    def image_callback(self, msg):
        
        cv_image = self.bridge.compressed_imgmsg_to_cv2(msg, "bgr8")
        bgr, self.ranked_arucos = self.run(cv_image)
        bgr2 , self.qrs = self.run2(cv_image)

        # convert tvec to tuple
        for key in self.ranked_arucos:
            try:
                self.ranked_arucos[key] = tuple(self.ranked_arucos[key].tolist())
            except:
                pass

        for i, qrs in enumerate(self.qrs):
            for key in qrs:
                try:
                    self.qrs[i][key] = tuple(qrs[key].tolist())
                except:
                    pass
            
        cv2.imshow("Imagem", bgr)
        cv2.imshow("QR CODES" , bgr2)
        cv2.waitKey(1)


    def control(self):
        msg = String()
        msg2 = String()

        msg.data = json.dumps(self.ranked_arucos)
        msg2.data = json.dumps(self.qrs)
        #print(self.qrs)
        #print(msg.data)
        print(msg2.data)

        #print('O número de Arucos encontrados é: ' , len(msg.data))
        
        self.qrs_pub.publish(msg2)
        self.creeper_pub.publish(msg)
        
            
def main(args=None):
    rclpy.init(args=args)
    ros_node = Creepers() 

    rclpy.spin(ros_node)

    ros_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()


    