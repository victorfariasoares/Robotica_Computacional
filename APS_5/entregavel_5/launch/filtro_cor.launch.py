from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='entregavel_5',
            executable='filtro_cor',
            name='filtro_cor'),
    ],)