#-*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(
    name='balbec',
    version='0.5',
    description='A nagios frontend, which makes things looks nicer. Provides HTML and XML.',
    author='Magnus Kulke',
    author_email='',
    url='https://github.com/mkulke/balbec',
    packages=find_packages(),
    install_requires=[
        'lxml',
        'twisted>=0.11',
    ],
    entry_points={
        'console_scripts': [
            'balbec-www = balbec_twisted:main',
        ]
    },
)