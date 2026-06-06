import os
from glob import glob
from setuptools import find_packages, setup

package_name = "core_monitors"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        (
            "share/ament_index/resource_index/packages",
            ["resource/" + package_name],
        ),
        ("share/" + package_name, ["package.xml"]),
        # CRITICAL FIX: Installs all .launch.py files to the shared install/ share directory
        (
            os.path.join("share", package_name, "launch"),
            glob(os.path.join("launch", "*.launch.py")),
        ),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="your_name",
    maintainer_email="your@email.com",
    description="Core monitors package for ROS 2",
    license="Apache-2.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "health_monitor = core_monitors.system_health:main",
            "sensor_stream = core_monitors.sensor_stream:main",
            "safety_processor = core_monitors.safety_processor:main",
            "kinematic_service = core_monitors.kinematic_service:main",
            "docking_action_server = core_monitors.docking_action_server:main",
            "telemetry_broadcaster = core_monitors.telemetry_broadcaster:main",
            "diagnostics_monitor = core_monitors.diagnostics_monitor:main",
            "stress_test_server = core_monitors.stress_test_server:main",
            "fault_injector = core_monitors.fault_injector:main",
        ],
    },
)
