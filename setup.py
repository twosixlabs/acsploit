"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='acsploit',
    version='1.0.0',
    description='A tool for generating worst-case inputs for algorithms',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/twosixlabs/acsploit',
    author='Two Six Technologies',

    packages=find_packages(),

    python_requires='>=3.5, <4',

    install_requires=[
        'colorama',
        'cmd2',
        'delayed-assert',
        'exrex',
        'graphviz',
        'more-itertools',
        'netifaces',
        'pdoc3',
        'ply',
        'pypng',
        'pytest-cov',
        'pytest-xdist',
        'python-utils',
        'requests',
        'scapy',
        'scipy',
        'tqdm',
        'z3-solver',
    ],

    # If there are data files included in your packages that need to be
    # installed, specify them here.
    package_data={  # Optional
        'acsploit.exploits': [
            'exploits/bombs/compression/bombs-DONOTOPEN/*.gz',
            'exploits/bombs/compression/bombs-DONOTOPEN/zip_recursive.zip',
            'exploits/bombs/git/git_bombs/*.gz',
            'exploits/bombs/images/badsize.dat',
            'exploits/bombs/images/jpeg_bombs/*/*.jpeg',
            'exploits/bombs/xml/xml_bomb_template.txt',
            'exploits/bombs/fork/fork_bombs/fork-bomb.*',
            'exploits/bombs/fork/fork_bombs/fork-bomb.*',
        ],
    },

    entry_points={
        'console_scripts': [
            'acsploit=acsploit.__main__:main',
            'acsploit-test=acsploit.test.test_acsploit:test_acsploit_init',
        ],
    },

)
