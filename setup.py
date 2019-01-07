#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='res_manager',
    version='2.1.2',
    description=(
        'This tool helps you to manage your experimental results in a more elegant way, saving your experiment data by pickle with some high-level interfaces to save, load and preview.'
    ),
    long_description=open('README.rst').read(),
    author='Hongshan Li',
    author_email='lhs17@mails.tsinghua.edu.cn',
    maintainer='',
    maintainer_email='',
    license='GPL License',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/hosea1008/res_manager',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities'
    ],
    install_requires=['prettytable>=0.7.2']
)