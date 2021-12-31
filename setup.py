from setuptools import setup
import sys


if sys.version_info.major < 3:
    sys.exit('Python < 3 is unsupported (for now).')
    

def readfile(filename):
    with open(filename, 'r+') as f:
        return f.read()


setup(
    name="TUIFIManager",
    version="1.0.0",
    description="TUIFIManager, a terminal based file manager, meant to be used with a Uni-Curses project or as is",
    long_description=readfile('README.md'),
    author="George Chousos",
    author_email="gxousos@gmail.com",
    url="https://github.com/GiorgosXou/TUIFIManager",
    packages=['TUIFIManager'],
    install_requires=['Uni-Curses>=2.0.4'],
    entry_points={
        'console_scripts': [
            'tuifi = TUIFIManager.__main__:main'
        ]
    },
)
