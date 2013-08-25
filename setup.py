from setuptools import setup, find_packages

setup(
    name = "isaikootu",
    version = "0.1",
    url = 'http://github.com/tamizhgeek/isaikootu',
    license = 'BSD',
    description = "Indexer and Searcher for multimedia files",
    author = 'Azhagu Selvan',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ['setuptools','peewee'],
)
