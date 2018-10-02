from setuptools import setup

with open('README.md', 'r') as readme:
    LONG_DESCRIPTION = readme.read()

setup(
    name='csvprint',
    version='0.5.0',
    description='Print csv files in columnated format, either plain or as a Markdown or LaTeX table',
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