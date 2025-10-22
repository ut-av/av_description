"""Simple state publisher that listens for drive commands and publishes
front-wheel steering joint states.

Listens to topic: 'vesc_drive' (geometry_msgs/TwistStamped)
Publishes: 'joint_states' (sensor_msgs/JointState) with names
  - 'wheel_fl_connect'
  - 'wheel_fr_connect'

The node computes steering angle using the same formula as the C++ driver:
  steering_angle = atan(wheelbase / turn_radius)
where turn_radius = linear_velocity / angular_z (if angular_z != 0).
"""

from math import atan2, atan, fabs
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from sensor_msgs.msg import JointState
from geometry_msgs.msg import TwistStamped


class SteeringStatePublisher(Node):
    def __init__(self):
        super().__init__("steering_state_publisher")

        qos = QoSProfile(depth=10)
        self.joint_pub = self.create_publisher(JointState, "joint_states", qos)

        # parameter for wheelbase (meters). Default to 0.2 if not provided.
        self.declare_parameter("wheelbase", 0.2)
        self.wheelbase = float(self.get_parameter("wheelbase").value)

        # current steering angle
        self.steering_angle = 0.0

        # subscribe to vesc_drive
        self.create_subscription(TwistStamped, "vesc_drive", self.drive_callback, qos)

        # publish at 30Hz even if we don't receive messages, so viewers see joint state
        self.timer = self.create_timer(1.0 / 30.0, self.publish_joints)

        self.get_logger().info(
            f"steering_state_publisher started (wheelbase={self.wheelbase} m)"
        )

    def drive_callback(self, msg: TwistStamped):
        # Read linear.x and angular.z (z is rotational velocity about z axis)
        linear_x = msg.twist.linear.x
        angular_z = msg.twist.angular.z

        # Calculate steering angle using same logic as VescDriver::CalculateSteeringAngle
        steering_angle = 0.0
        if angular_z != 0 and linear_x != 0:
            # turn_radius = lin_vel / rot_vel; steering = atan(wheelbase / turn_radius)
            turn_radius = linear_x / angular_z
            if turn_radius != 0:
                steering_angle = atan(self.wheelbase / turn_radius)
        # if linear_x is zero but angular_z non-zero, we cannot compute a radius; leave angle unchanged

        self.steering_angle = steering_angle

    def publish_joints(self):
        js = JointState()
        now = self.get_clock().now().to_msg()
        js.header.stamp = now
        js.name = ["wheel_fl_connect", "wheel_fr_connect"]
        js.position = [self.steering_angle, self.steering_angle]
        self.joint_pub.publish(js)


def main(args=None):
    rclpy.init(args=args)
    node = SteeringStatePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
