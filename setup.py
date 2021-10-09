import os
from setuptools import setup


def read_file(filename):

    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name='photo-collage-tool',
    version='',
    author='',
    author_email='',
    description=(''),
    license='GPL3',
    keywords='',
    url='',
    packages=['application', 'tests'],
    long_description=read_file('readme.md'),
    classifiers=[
        'Development Status :: Beta',
        'Topic :: Utilities',
        'License :: OSI Approved :: GPL3'
        ]
    )
