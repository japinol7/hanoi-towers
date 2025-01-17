from setuptools import setup

setup(
    name='hanoitowers',
    author='Joan A. Pinol  (japinol)',
    version='0.0.3',
    license='MIT',
    description="The Towers of Hanoi",
    long_description="The Towers of Hanoi",
    url='https://github.com/japinol7/hanoitowers',
    packages=['hanoitowers'],
    python_requires='>=3.13',
    install_requires=['pygame-ce'],
    entry_points={
        'console_scripts': [
            'hanoitowers=hanoitowers.__main__:main',
            ],
    },
)
