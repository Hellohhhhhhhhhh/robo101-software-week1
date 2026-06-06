import os
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription(
        [
            Node(
                package="core_monitors",
                executable="telemetry_broadcaster",
                name="telemetry_broadcaster_node",
                output="screen",
            ),
            Node(
                package="core_monitors",
                executable="diagnostics_monitor",
                name="diagnostics_monitor_node",
                output="screen",
            ),
            Node(
                package="core_monitors",
                executable="stress_test_server",
                name="stress_test_server_node",
                output="screen",
            ),
            Node(
                package="core_monitors",
                executable="fault_injector",
                name="fault_injector_node",
                output="screen",
            ),
        ]
    )
