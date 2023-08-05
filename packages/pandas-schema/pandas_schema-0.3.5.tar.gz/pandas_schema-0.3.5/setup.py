#!/usr/bin/env python
import distutils
import os
import subprocess
from pathlib import Path

from setuptools import setup, find_packages

here = Path(__file__).parent
readme = (here / 'README.rst')

# Get the long description from the README file
if readme.exists():
    with readme.open() as readme:
        long_description = readme.read()
else:
    long_description = ''

# Parse out the version from version.py
version = {}
with open("pandas_schema/version.py") as fp:
    exec(fp.read(), version)


class BuildReadme(distutils.cmd.Command):
    description = 'Build the README.rst file'
    user_options = []

    def initialize_options(self): pass

    def finalize_options(self): pass

    def run(self):
        command = ['sphinx-build', '-b', 'rst', 'doc/readme', str(here)]
        self.announce(
            'Running command: {}'.format(command),
            level=distutils.log.INFO
        )
        subprocess.check_call(command, cwd=str(here))


class BuildHtmlDocs(distutils.cmd.Command):
    description = 'Build the HTML docs for GitHub Pages'
    user_options = [
        # The format is (long option, short option, description).
        ('dir=', 'd', 'The directory in which to build the docs'),
    ]

    def initialize_options(self):
        self.dir = '.'

    def finalize_options(self):
        if self.dir:
            assert os.path.isdir(self.dir), ('Specified directory "{}" does not exist'.format(self.dir))

    def run(self):
        command = ['sphinx-build', '-b', 'html', 'doc/site', self.dir]
        self.announce(
            'Running command: {}'.format(command),
            level=distutils.log.INFO
        )
        subprocess.check_call(command, cwd=str(here))


setup(
    name='pandas_schema',
    version=version['__version__'],
    description='A validation library for Pandas data frames using user-friendly schemas',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/TMiguelT/PandasSchema',
    author='Michael Milton',
    author_email='michael.r.milton@gmail.com',
    license='MIT',
    test_suite='test',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='pandas csv verification schema',
    packages=find_packages(include=['pandas_schema']),
    install_requires=['numpy', 'pandas>=0.19'],
    cmdclass={
        'build_readme': BuildReadme,
        'build_site': BuildHtmlDocs
    }
)
