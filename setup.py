from setuptools import setup
setup(
    name='pynotes',
    version='0.1.0',
    packages=['pynotes'],
    entry_points={
        'console_scripts': [
            'pynotes = pynotes.__main__:main'
        ]
    })
