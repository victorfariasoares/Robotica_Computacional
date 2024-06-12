from setuptools import find_packages, setup
import os
from glob import glob


package_name = 'entregavel_3'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name), glob('launch/*.launch.py'))

    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='borg',
    maintainer_email='vinicius.cezimbra.miranda@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
                'quadrado =   entregavel_3.quadrado:main',
                'indeciso =   entregavel_3.indeciso:main',
                'limpador =   entregavel_3.limpador:main',
                'modo_sobrevivencia  = entregavel_3.modo_sobrevivencia:main'
        ],
    },
)
