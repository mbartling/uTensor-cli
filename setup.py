import os
from setuptools import setup

LONG_DESC = open('README.md').read()
LICENSE = open('LICENSE').read()

repository_dir = os.path.dirname(__file__)

with open(os.path.join(repository_dir, 'requirements.txt')) as fh:
    dependencies = fh.readlines()

setup(
        name="uTensor-cli",
        version="0.0.1",
        description="Command line tools for running tensorflow models on mbed devices",
        dependency_links=['http://github.com/neil-tan/tf-node-viewer/tarball/master#egg=tf-node-viewer'],
        long_description=LONG_DESC,
        url='https://github.com/mbartling/uTensor-cli',
        author='Michael Bartling',
        author_email='michael.bartling15@gmail.com',
        license=LICENSE,
        packages=["utensor"],
        entry_points={
            'console_scripts': [
                'mbed=utensor.utensor:main',
                'mbed-cli=utensor.utensor:main',
                ]
            },
)
