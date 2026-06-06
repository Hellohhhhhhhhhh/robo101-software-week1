#!/usr/bin/env python3
import random
import time
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from example_interfaces.action import Fibonacci


class StressTestServer(Node):

    def __init__(self) -> None:
        super().__init__("stress_test_server")
        self._action_server = ActionServer(
            self, Fibonacci, "run_stress_test", self.execute_callback
        )
        self.get_logger().info("Diagnostic Stress Test Action Server online.")

    def execute_callback(self, goal_handle) -> Fibonacci.Result:
        self.get_logger().info("Executing system stress test (10 seconds)...")
        feedback_msg = Fibonacci.Feedback()
        fault_score = 0.0

        for elapsed in range(1, 11):
            time.sleep(1.0)  # Safe inside isolated action thread context
            fault_score += random.uniform(5.0, 15.0)

            # Pack elapsed time and fault score as integers into the sequence array
            feedback_msg.sequence = [elapsed, int(fault_score)]
            goal_handle.publish_feedback(feedback_msg)
            self.get_logger().info(
                f"Progress: {elapsed}s/10s | Accumulating Fault Score: {int(fault_score)}"
            )

        goal_handle.succeed()
        result = Fibonacci.Result()

        # If fault score exceeds 75, fail the stress test
        if fault_score > 75.0:
            result.sequence = [0]  # Representing FAIL
            self.get_logger().error("STRESS TEST COMPLETE: STATUS -> FAIL")
        else:
            result.sequence = [1]  # Representing PASS
            self.get_logger().info("STRESS TEST COMPLETE: STATUS -> PASS")

        return result


def main(args=None):
    rclpy.init(args=args)
    node = StressTestServer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
