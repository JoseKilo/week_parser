import os

from setuptools import setup


BASE_DIR = os.path.dirname(__file__)

with open(os.path.join(BASE_DIR, 'requirements.txt')) as requirements:
    REQUIREMENTS = requirements.read().split('\n')


setup(
    name='week_parser',
    packages=['week_parser'],
    include_package_data=True,
    install_requires=REQUIREMENTS,
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
    entry_points={
        'console_scripts': [
            'week_parser=week_parser.main:main',
        ],
    },
)
