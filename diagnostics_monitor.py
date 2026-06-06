#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from std_srvs.srv import Trigger


class DiagnosticsMonitor(Node):

    def __init__(self) -> None:
        super().__init__("diagnostics_monitor")

        self.history = []
        self.warning_count = 0
        self.error_count = 0

        # Sub to telemetry
        self.sub = self.create_subscription(
            Float64MultiArray, "/robot_telemetry", self.telemetry_callback, 10
        )

        # Expose service endpoint
        self.srv = self.create_service(
            Trigger, "/get_health_report", self.handle_health_report
        )
        self.get_logger().info("Diagnostics Monitor online with rolling history loop.")

    def telemetry_callback(self, msg: Float64MultiArray) -> None:
        if len(msg.data) < 4:
            return

        battery, cpu_temp, left_rpm, right_rpm = msg.data

        # Keep a strict rolling window of the last 10 items
        self.history.append(msg.data)
        if len(self.history) > 10:
            self.history.pop(0)

        # Threshold Evaluations
        if battery < 11.5:
            self.get_logger().warn(f"LOW BATTERY: {battery:.2f} V")
            self.warning_count += 1

        if cpu_temp > 85.0:
            self.get_logger().error(f"CPU OVERHEATING: {cpu_temp:.1f}°C")
            self.error_count += 1

        if abs(left_rpm - right_rpm) > 50.0:
            self.get_logger().warn(
                f"WHEEL SLIP DETECTED! Delta: {abs(left_rpm - right_rpm):.1f} RPM"
            )
            self.warning_count += 1

    def handle_health_report(self, request, response) -> Trigger.Response:
        if not self.history:
            response.success = False
            response.message = "No telemetry data received yet."
            return response

        # Compute averages over rolling buffer
        count = len(self.history)
        avg_bat = sum(d[0] for d in self.history) / count
        avg_cpu = sum(d[1] for d in self.history) / count

        response.success = True
        response.message = (
            f"\n--- HEALTH REPORT (Last {count} frames) ---\n"
            f"Total Warnings Caught: {self.warning_count}\n"
            f"Total Errors Caught: {self.error_count}\n"
            f"Rolling Avg Battery: {avg_bat:.2f} V\n"
            f"Rolling Avg CPU Temp: {avg_cpu:.1f}°C"
        )
        return response


def main(args=None):
    rclpy.init(args=args)
    node = DiagnosticsMonitor()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
