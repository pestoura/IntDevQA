# setup.py

from setuptools import setup, find_packages

setup(
    name='folder-sync',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'requests==2.26.0',
        'numpy==1.21.1',
    ],
    entry_points={
        'console_scripts': [
            'folder-sync = src.sync:main',
        ],
    },
    author='Pedro Estoura',
    author_email='pedro.estoura',
    description='A Python tool for folder synchronization',
    url='https://github.com/your-username/folder-sync',
    license='MIT',
)
