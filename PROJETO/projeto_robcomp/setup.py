from setuptools import find_packages, setup

package_name = 'projeto_robcomp'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='borg',
    maintainer_email='venanciofaf@al.insper.edu.br',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'creepers = projeto_robcomp.creeper_pub:main',
            'reconhecedor = projeto_robcomp.reconhecedor:main',
            'derrubador = projeto_robcomp.derrubador:main',
            'drop_area = projeto_robcomp.droparea_pub:main',
            'guardador = projeto_robcomp.guardador:main'
        ],
    },
)
