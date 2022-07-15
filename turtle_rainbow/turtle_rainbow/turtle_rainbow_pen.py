from turtlesim.msg import Pose
from turtlesim.srv import SetPen

from example_interfaces.srv import SetBool
import rclpy
from rclpy.node import Node
import math

class ChangePen(Node):
    def __init__(self):
        super().__init__('turtle_rainbow')
        queue_size = 10
        self.start_x = 5.0
        self.start_y = 5.0
        self.flag = 0
        self.color_flag = 0
        self.length = 0.5
        self.color = [0xff0000,0xff8c00,0xffff00,0x008000,0x0000ff,0x4b0082,0x800080]
        self.client = self.create_client(SetPen, 'turtle1/set_pen')
        self.pose_subscriber = self.create_subscription(
            Pose, 'turtle1/pose', self.sub_callback, queue_size
        )
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, Waiting again...')

        self.req = SetPen.Request()
        self.get_logger().info('=== [Ready to Call Service Request] ===')

    def sub_callback(self, msg):
        if self.flag==0:
            self.start_x = msg.x
            self.start_y = msg.y
            self.flag = 1
        elif self.flag==1:
            if math.sqrt(math.pow(msg.x-self.start_x,2)+math.pow(msg.y-self.start_y,2)) > self.length :
                self.send_request()
                self.flag = 2
        elif self.flag==2 and self.future.done(): 
            self.flag = 0
            
    def send_request(self):
        self.req.r = (self.color[self.color_flag]&0xff0000)>>16
        self.req.g = (self.color[self.color_flag]&0xff00)>>8
        self.req.b = (self.color[self.color_flag]&0xff)
        self.req.width = 10
        self.color_flag = (self.color_flag+1)%7
        self.future = self.client.call_async(self.req)
    def __del__(self):
        self.req.r = 180
        self.req.g = 180
        self.req.b = 180
        self.req.width = 3
        self.future = self.client.call_async(self.req)

def main(args=None):
    rclpy.init(args=args)

    turtle_rainbow = ChangePen()

    rclpy.spin(turtle_rainbow)
    turtle_rainbow.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
