# !/usr/bin/env/ python3
#
# Copyright 2021 @RoadBalance
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from turtlesim.msg import Pose
from turtlesim.srv import SetPen

from example_interfaces.srv import SetBool
import rclpy
from rclpy.node import Node
import math


# example_interfaces/srv/SetBool srv Description.
#
# bool data # e.g. for hardware enabling / disabling
# ---
# bool success   # indicate successful run of triggered service
# string message # informational, e.g. for error messages


class ChangePen(Node):

    def __init__(self):
        super().__init__('turtle_rainbow')
        #self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
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

def main(args=None):
    rclpy.init(args=args)

    turtle_rainbow = ChangePen()    ##여기서 요청 

    rclpy.spin(turtle_rainbow)

    turtle_rainbow.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
