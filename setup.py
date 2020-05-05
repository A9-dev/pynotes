from setuptools import setup, find_packages
setup(
    name='pynotes',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pynotes = pynotes.__main__:main'
        ]
    })
