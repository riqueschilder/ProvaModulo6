#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time


class TurtleController(Node):
    def __init__(self):
        super().__init__('turtle_controller')
        self.publisher_ = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        self.timer_ = self.create_timer(0.1, self.move_turtle)
        self.twist_msg_ = Twist()
        self.path_queue = [(0.0, 0.5), (0.5, 0.0), (0.0, 0.5), (0.5, 0.0), (0.0, 1.0), (1.0, 0.0)]
        self.path_stack = []

    def move_turtle(self):
        if len(self.path_queue) > 0:
            next_point = self.path_queue.pop(0)
            self.twist_msg_.linear.x = next_point[0]
            self.twist_msg_.linear.y = next_point[1]
            self.publisher_.publish(self.twist_msg_)
            self.path_stack.append((-next_point[0], -next_point[1]))
            time.sleep(1)
        elif len(self.path_stack) > 0:
            next_point = self.path_stack.pop()
            self.twist_msg_.linear.x = next_point[0]
            self.twist_msg_.linear.y = next_point[1]
            self.publisher_.publish(self.twist_msg_)
            time.sleep(1)
        else:
            self.twist_msg_.linear.x = 0.0
            self.twist_msg_.linear.y = 0.0
            self.publisher_.publish(self.twist_msg_)
            time.sleep(1)
        

def main(args=None):
    rclpy.init()
    turtle_controller = TurtleController()
    rclpy.spin(turtle_controller)
    turtle_controller.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
