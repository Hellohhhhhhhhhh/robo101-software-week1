#!/usr/bin/env python3
import random
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray


class TelemetryBroadcaster(Node):

    def __init__(self) -> None:
        super().__init__("telemetry_broadcaster")
        self.publisher_ = self.create_publisher(
            Float64MultiArray, "/robot_telemetry", 10
        )
        self.timer = self.create_timer(0.5, self.publish_telemetry)
        self.get_logger().info("Telemetry Broadcaster active streaming at 2 Hz.")

    def publish_telemetry(self) -> None:
        msg = Float64MultiArray()

        # Simulate fluctuating robot states
        battery = random.uniform(10.5, 14.2)  # Healthy & Low battery bounds
        cpu_temp = random.uniform(50.0, 92.0)  # Healthy & Overheating bounds
        left_rpm = random.uniform(100.0, 150.0)
        # Randomly inject a wheel slip delta
        right_rpm = left_rpm + random.uniform(-60.0, 60.0)

        msg.data = [battery, cpu_temp, left_rpm, right_rpm]
        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = TelemetryBroadcaster()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
