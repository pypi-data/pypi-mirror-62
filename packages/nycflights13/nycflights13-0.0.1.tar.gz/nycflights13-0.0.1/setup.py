from setuptools import setup, find_namespace_packages

VERSION = '0.0.1'

setup(
    name='nycflights13',
    packages=find_namespace_packages(),
    version=VERSION,
    description='A data package for nyc flights (the nycflights13 R package)',
    author='Michael Chow',
    license='CC0',
    author_email='mc_al_github@fastmail.com',
    url='https://github.com/machow/nycflights13',
    keywords=['package', ],
    install_requires=[
        "pandas>=0.24.0",
    ],
    python_requires=">=3.5",
    package_data={'nycflights13': ['data/*.csv*']},
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
