#!/usr/bin/env python
# coding=utf-8
from setuptools import setup, find_packages

setup(
    name='res_manager',
    version='3.1.1',
    description=(
        'res-manager helps you to manage your experimental results data in a more convenient way.'
    ),
    long_description=open('README.rst').read(),
    author='Hongshan Li',
    author_email='lhs17@mails.tsinghua.edu.cn',
    maintainer='',
    maintainer_email='',
    license='GPLv3',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/hosea1008/res_manager',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    install_requires=['prettytable>=0.7.2']
)
