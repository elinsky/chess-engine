from setuptools import setup, find_packages

setup(
    name='chess_engine',
    version='0.0.1',
    url='https://github.com/elinsky/chess_engine',
    author='Brian Elinsky',
    packages=find_packages(),
    install_requires=['chess >= 1.7.0', 'numpy >= 1.21.4'],
)
