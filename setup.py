from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name = "isaikootu",
    version = "0.1",
    url = 'http://github.com/tamizhgeek/isaikootu',
    license = 'BSD',
    description = "Indexer and Searcher for multimedia files",
    long_description = readme(),
    author = 'Azhagu Selvan',
    packages = ['isaikootu'],
    scripts = ['bin/isaikootu'],
    install_requires = ['setuptools>=0.9','peewee', 'prettytable', 'eyed3', 'cmdln'],
    zip_safe = False,
    test_suite='nose.collector',
    tests_require=['nose'],
)
