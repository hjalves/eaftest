#!/usr/bin/env python

from setuptools import setup

setup(
    name='eaftest',
    version='0.1.dev1',
    description=('Tools to perform hypothesis tests based on '
                 'the empirical attainment function (EAF).'),
    url='https://bitbucket.org/hjalves/eaftest',
    author='Humberto Alves',
    author_email='halves@uc.pt',
    license='GPL',
    classifiers=[
        'Development Status :: 1 - Planning',
        #'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='eaf statistics opencl',
    packages=['eaftest'],
    install_requires=[
        'numpy',
        'pyopencl',
    ],
    entry_points={
        'console_scripts': [
            'eaftest=eaftest.cmd:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)