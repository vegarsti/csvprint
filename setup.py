from setuptools import setup

with open('README.rst', 'r') as readme:
    LONG_DESCRIPTION = readme.read()

setup(
    name='csvprint',
    version='0.2.0',
    description='Pretty-printer for csv files, including in Markdown format',
    long_description=LONG_DESCRIPTION,
    packages=['csvprint'],
    license='MIT',
    scripts=['bin/csvprint'],
    author='Vegard Stikbakke',
    author_email='vegard.stikbakke@gmail.com',
    url='https://github.com/vegarsti/csvprint',
    keywords='csv',
)