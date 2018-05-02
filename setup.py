from setuptools import setup

with open('README.md', 'r') as readme:
    LONG_DESCRIPTION = readme.read()

setup(
    name='csvprint',
    version='0.3.2',
    description='Print csv files in columnated format, can also output in Markdown and LaTeX format',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=['csvprint'],
    license='MIT',
    scripts=['bin/csvprint'],
    author='Vegard Stikbakke',
    author_email='vegard.stikbakke@gmail.com',
    url='https://github.com/vegarsti/csvprint',
    keywords='csv',
)