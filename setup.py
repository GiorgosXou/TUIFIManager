from setuptools import setup
import sys


if sys.version_info.major < 3:
    sys.exit('Python < 3 is unsupported (for now).')
    

#def readfile(filename):
#    with open(filename, 'r+') as f:
#        return f.read()


setup(
    name="TUIFIManager",
    version="2.0.5",
    description="A cross-platform terminal-based termux-oriented file manager (and component), meant to be used with a Uni-Curses project or as is. This project is mainly an attempt to get more attention to the Uni-Curses project.",
    #long_description=readfile('README.md'),
    author="George Chousos",
    author_email="gxousos@gmail.com",
    url="https://github.com/GiorgosXou/TUIFIManager",
    packages=['TUIFIManager'],
    install_requires=['Uni-Curses>=2.1.0'],
    entry_points={
        'console_scripts': [
            'tuifi = TUIFIManager.__main__:main'
        ]
    },
)

# pip3 install .
# python setup.py sdist
# twine upload dist/*
