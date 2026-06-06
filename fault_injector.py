#!/usr/bin/env python3
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from example_interfaces.action import Fibonacci


class FaultInjector(Node):

    def __init__(self) -> None:
        super().__init__("fault_injector")
        self._action_client = ActionClient(self, Fibonacci, "run_stress_test")
        self.timer = self.create_timer(2.0, self.send_goal_once)
        self.goal_sent = False

    def send_goal_once(self) -> None:
        if self.goal_sent:
            return
        self.timer.cancel()

        if not self._action_client.wait_for_server(timeout_sec=5.0):
            self.get_logger().error("Stress test server not visible!")
            return

        self.goal_sent = True
        goal_msg = Fibonacci.Goal()
        goal_msg.order = 10  # Duration order config

        self.get_logger().info("Dispatching Stress Test request to server...")
        send_goal_future = self._action_client.send_goal_async(
            goal_msg, feedback_callback=self.feedback_callback
        )
        send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future) -> None:
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error("Stress test goal rejected by server.")
            return
        self.get_logger().info("Goal accepted by server, monitoring feedback...")
        self.result_future = goal_handle.get_result_async()
        self.result_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback_msg) -> None:
        data = feedback_msg.feedback.sequence
        if len(data) >= 2:
            self.get_logger().info(
                f"[FEEDBACK] Time: {data[0]}s | Current Fault Score: {data[1]}"
            )

    def get_result_callback(self, future) -> None:
        result = future.result().result
        status_code = result.sequence[0]
        if status_code == 1:
            self.get_logger().info("🌟 FINAL RESULT RECEIVED: PLATFORM PASSED")
        else:
            self.get_logger().error("🚨 FINAL RESULT RECEIVED: PLATFORM FAILED")


def main(args=None):
    rclpy.init(args=args)
    node = FaultInjector()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
