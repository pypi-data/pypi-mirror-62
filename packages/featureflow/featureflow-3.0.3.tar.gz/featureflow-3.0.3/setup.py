from setuptools import setup
import re
import subprocess

try:
    long_description = subprocess.check_output(
        'pandoc --to rst README.md', shell=True).decode('utf-8')
except(IOError, ImportError, subprocess.CalledProcessError) as e:
    long_description = open('README.md').read()


with open('featureflow/__init__.py', 'r') as fd:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
        fd.read(),
        re.MULTILINE).group(1)

download_url = 'https://github.com/jvinyard/featureflow/tarball/{version}' \
    .format(**locals())

setup(
    name='featureflow',
    version=version,
    url='https://github.com/JohnVinyard/featureflow',
    author='John Vinyard',
    author_email='john.vinyard@gmail.com',
    long_description=long_description,
    packages=['featureflow'],
    download_url=download_url,
    install_requires=[
        'dill',
        'nose',
        'unittest2',
        'certifi==2017.7.27.1',
        'requests',
        'lmdb',
        'redis'
    ],
    extras_require={
        'numpy': ['numpy==1.15.3']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
