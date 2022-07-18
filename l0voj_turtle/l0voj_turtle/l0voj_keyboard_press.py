import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist

import sys, select, termios, tty

settings = termios.tcgetattr(sys.stdin)

def getKey_sys():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

class ChangePen(Node):
	def __init__(self):					
		super().__init__('l0voj_keyboard_test')
	def setKey_node(self, key):
		self._key = key
	def showKey_node(self):
		self.get_logger().info(self._key)

def main(args=None):
	rclpy.init(args=args)
	turtle_rainbow = ChangePen()
	while(True):
		key = getKey_sys()
		if key == '\x03':
			break
		else:	
			turtle_rainbow.setKey_node(key) ##조건 : 키를 받는다
			turtle_rainbow.showKey_node()
		#rclpy.spin_once(turtle_rainbow) ##한번만 실행되게 한다 대신 이걸 while문에 씌운다 그리고 키 입력과 함께 돌린다
	turtle_rainbow.destroy_node()
	rclpy.shutdown()
	    
if __name__ == '__main__':
	main()

