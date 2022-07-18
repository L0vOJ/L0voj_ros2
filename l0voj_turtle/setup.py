from setuptools import setup

package_name = 'l0voj_turtle'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='l0voj',
    maintainer_email='wonjjw98@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'turtle_rainbow = l0voj_turtle.turtle_rainbow_pen:main',
            'teleop_twist_keyboard_sample = l0voj_turtle.keyboard_press_sample:main',
            'l0voj_keyboard_test = l0voj_turtle.l0voj_keyboard_press:main'
        ],
    },
)
