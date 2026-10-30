#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""任务一-5：用 ROS2 控制小海龟(turtlesim)画正方形。

运行前先开两个终端：
  终端1: source /opt/ros/humble/setup.bash && ros2 run turtlesim turtlesim_node
  终端2: source /opt/ros/humble/setup.bash && python3 turtle_square.py
"""
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class SquareDrawer(Node):
    def __init__(self):
        super().__init__('square_drawer')
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.step)
        self.phase = 0        # 0=直行, 1=转向
        self.side = 0         # 已完成的边数
        self.t = 0.0
        self.speed = 1.5      # 直行速度
        self.turn_speed = 1.5708   # 每秒 90 度
        self.move_time = 2.0       # 直行 2 秒
        self.turn_time = 1.0       # 转向 1 秒

    def step(self):
        if self.side >= 4:          # 4 条边画完就停
            self.pub.publish(Twist())
            self.timer.cancel()
            self.get_logger().info('正方形画完！')
            return

        msg = Twist()
        if self.phase == 0:         # 直行
            msg.linear.x = self.speed
            self.t += 0.1
            if self.t >= self.move_time:
                self.t = 0.0
                self.phase = 1
        else:                       # 转向 90 度
            msg.angular.z = self.turn_speed
            self.t += 0.1
            if self.t >= self.turn_time:
                self.t = 0.0
                self.phase = 0
                self.side += 1
        self.pub.publish(msg)


def main():
    rclpy.init()
    node = SquareDrawer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
