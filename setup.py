from distutils.core import setup

setup(
    name='contextual-lexicon',
    version='0.1.0',
    author='Michael McAuliffe',
    author_email='michael.e.mcauliffe@gmail.com',
    packages=['conlex'],
    url='http://pypi.python.org/pypi/contextual-lexicon/',
    license='LICENSE.txt',
    description='Graph database representing contextual links between words for querying shared contexts',
    long_description=open('README.md').read(),
    install_requires=['bulbs'],
)
