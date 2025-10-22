from setuptools import find_packages, setup

package_name = "roboracer_description"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        # install launch files
        ("share/" + package_name + "/launch", ["launch/description.launch.py"]),
        # install urdf and meshes
        ("share/" + package_name + "/urdf", ["urdf/roboracer.urdf.xml"]),
        (
            "share/" + package_name + "/meshes",
            [
                "meshes/base.stl",
                "meshes/body.stl",
                "meshes/camera.stl",
                "meshes/hokuyo_ust-10xl.stl",
                "meshes/wheel.stl",
            ],
        ),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Nathan Tsoi",
    maintainer_email="nathan@vertile.com",
    description="Robot description files for the RoboRacer 1/10th scale autonomous racecar",
    license="MIT",
    extras_require={
        "test": [
            "pytest",
        ],
    },
    entry_points={
        "console_scripts": [
            "state_publisher = roboracer_description.state_publisher:main",
        ],
    },
)
