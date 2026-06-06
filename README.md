# robo101-software-week1
Multi-Node Robot Diagnostics Dashboard 🚀

Robo101 Robotics Club (IIT Guwahati) — Weekend Task 1 (Week 1)

This repository contains a fully integrated, multi-node robot diagnostics and monitoring network built on ROS 2 Humble. Rather than testing communication architectures in isolation, this system demonstrates how Topics (Publisher/Subscriber), Services (Request-Response), and Actions (Goal-Feedback-Result) operate concurrently to monitor real-time subsystems, query metrics on-demand, and manage long-running diagnostic stress routines without a single point of failure.

🗺️ System Architecture

The ecosystem consists of four decoupled ROS 2 nodes executing concurrently under a unified launch profile:

    +-------------------------------------------------------------+
    |                  telemetry_broadcaster                      |
    |  [Publishes raw sensor vectors on /robot_telemetry @ 2Hz]   |
    +------------------------------+------------------------------+
                                   |
                                   | (Float64MultiArray Message)
                                   v
    +-------------------------------------------------------------+
    |                   diagnostics_monitor                       |
    |  - Logs WARNINGS/ERRORS against physical safety limits      |
    |  - Buffers a rolling history of the last 10 messages        |
    |  - Hosts /get_health_report service (std_srvs/srv/Trigger)  |
    +-------------------------------------------------------------+
                                   ^
                                   | (Triggers on-demand metrics)
                                   |
                         [ROS 2 CLI Service Call]

    ===============================================================

    +-------------------+                      +--------------------+
    |  fault_injector   | ----(Goal: Order)--->| stress_test_server |
    |  [Action Client]  | <---(Feedback: Seq)--|  [Action Server]   |
    |                   | <---(Result: Seq)----|  (Runs 10s Thread) |
    +-------------------+                      +--------------------+


📦 Node Directory & Responsibilities

telemetry_broadcaster (Publisher): Simulates real-world hardware by outputting float data vectors representing battery voltage, CPU temperature, and left/right wheel rotational velocities (RPM) to /robot_telemetry every 0.5 seconds.

diagnostics_monitor (Subscriber + Service Server): Continuously evaluates telemetry arrays against pre-defined safety bounds. It maintains a 10-frame sliding calculation history and exposes /get_health_report to deliver real-time metrics dynamically.

stress_test_server (Action Server): Spawns an isolated thread when triggered to run a 10-second high-load stress simulation, evaluating hardware reactions and returning a final performance verdict.

fault_injector (Action Client): Dispatches automated command goals to the action server, captures real-time diagnostic performance metrics, and logs final health states.

⚠️ Safety & Diagnostic Thresholds

The diagnostics_monitor enforces the following thresholds over the raw telemetry feed:

Condition Monitor

Evaluated Threshold

Log Output Level

Error Classification

Subsystem Voltage

Battery Voltage < 11.5 V

WARN

Low Power / Charge Required

Processor Thermal

CPU Temperature > 85.0 °C

ERROR

CPU Thermal Overheating Alert

Differential Kinematics

$\lvert \text{Left RPM} - \text{Right RPM} \rvert > 50.0$

WARN

Wheel Slip Detected

🛠️ Installation & Compilation

Ensure your development environment is running Ubuntu 22.04 LTS and ROS 2 Humble.

1. Workspace Configuration

Clone this repository directly into your ROS 2 workspace source directory:

# Navigate to your workspace source path
cd ~/intensive_ws/src

# Clone this repository
git clone [https://github.com/](https://github.com/)<your-username>/robo101-software-week1.git core_monitors


2. Compile and Source

Return to the workspace root, clear any legacy packages, and build the binaries:

# Navigate to workspace root
cd ~/intensive_ws

# Clean previous build artifacts
rm -rf build/core_monitors install/core_monitors

# Compile the packages
colcon build --packages-select core_monitors --symlink-install

# Register the workspace environment variables
source install/setup.bash


🚀 Execution Guide

This package includes a master launch script that configures logging parameters and automatically orchestrates the execution of all four nodes simultaneously.

Step 1: Fire up the Diagnostic Ecosystem (Terminal Pane 1)

Initialize the network from your sourced terminal window:

ros2 launch core_monitors diagnostics.launch.py


You should instantly see aggregated stdout reports of telemetry streams, active threshold alerts, and the asynchronous lifecycle of the action-based stress test.

Step 2: Query On-Demand Health Reports (Terminal Pane 2)

While the launch routine runs, open a secondary terminal pane, source your workspace, and query the diagnostics server:

source ~/intensive_ws/install/setup.bash
ros2 service call /get_health_report std_srvs/srv/Trigger


Expected Service Output Example:

requester: making request: std_srvs.srv.Trigger_Request()

response:
std_srvs.srv.Trigger_Response(
    success=True,
    message='\n--- HEALTH REPORT (Last 10 frames) ---\nTotal Warnings Caught: 50\nTotal Errors Caught: 21\nRolling Avg Battery: 12.61 V\nRolling Avg CPU Temp: 71.3°C'
)


🎯 Verified Acceptance Criteria

[CRITERION 1] Multi-Node Orchestration: Successfully triggers and coordinates all 4 nodes from a unified python launch description (diagnostics.launch.py).

[CRITERION 2] Interactive Diagnostic Reports: The /get_health_report trigger service processes and maps internal lists dynamically to output rolling metrics to the user.

[CRITERION 3] Asynchronous Action Diagnostics: The /run_stress_test action server safely manages a 10-second feedback loop in its own thread, printing real-time data updates before returning a terminal PASS or FAIL verdict.

[CRITERION 4] Decoupled Resiliency: Nodes are running as individual operating system processes. Terminating individual nodes will not crash the remaining active graph nodes.
