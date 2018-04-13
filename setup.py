#!/usr/bin/env python3
"""AbodePy setup script."""
from setuptools import setup, find_packages
from abodepy.helpers.constants import (__version__, PROJECT_PACKAGE_NAME,
                                       PROJECT_LICENSE, PROJECT_URL,
                                       PROJECT_EMAIL, PROJECT_DESCRIPTION,
                                       PROJECT_CLASSIFIERS, PROJECT_AUTHOR,
                                       PROJECT_LONG_DESCRIPTION)

PACKAGES = find_packages(exclude=['tests', 'tests.*'])

setup(
    name=PROJECT_PACKAGE_NAME,
    version=__version__,
    description=PROJECT_DESCRIPTION,
    long_description=PROJECT_LONG_DESCRIPTION,
    author=PROJECT_AUTHOR,
    author_email=PROJECT_EMAIL,
    license=PROJECT_LICENSE,
    url=PROJECT_URL,
    platforms='any',
    py_modules=['abodepy'],
    packages=PACKAGES,
    include_package_data=True,
    install_requires=[
        'requests>=2.12.4',
        'lomond==0.1.14',
        'colorlog==3.0.1',
    ],
    test_suite='tests',
    entry_points={
        'console_scripts': [
            'abodepy = abodepy.__main__:main'
        ]
    },
    classifiers=PROJECT_CLASSIFIERS
)
