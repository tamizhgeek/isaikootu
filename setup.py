from setuptools import setup
from setuptools.command.install import install as _install


def readme():
    with open('README') as f:
        return f.read()


class install(_install):
    def run(self):
        _install.run(self)



setup(
    cmdclass = {'install' : install},
    name = "isaikootu",
    version = "0.1",
    url = 'http://github.com/tamizhgeek/isaikootu',
    license = 'BSD',
    description = "Indexer and Searcher for multimedia files",
    long_description = readme(),
    author = 'Azhagu Selvan',
    packages = ['isaikootu'],
    scripts = ['bin/isaikootu'],
    install_requires = ['setuptools','peewee', 'prettytable', 'eyed3'],
    zip_safe = False,
    test_suite='nose.collector',
    tests_require=['nose'],
)
