from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'entregavel_5'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), 
            glob(os.path.join('launch', '*launch.[pxy][yma]*')))
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
            'segue_linha = entregavel_5.segue_linha:main',
            'aproxima = entregavel_5.aproxima:main',
            'filtro_cor = entregavel_5.filtro_cor:main',
        ],
    },
)
