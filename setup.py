import ast
import sys

from setuptools import find_packages, setup


def readme():
    try:
        with open('README.rst') as f:
            return f.read()
    except (IOError, OSError):
        return


def get_version():
    filename = 'tsukkomi/__init__.py'
    version = None
    with open(filename, 'r') as f:
        tree = ast.parse(f.read(), filename)
        for node in tree.body:
            if (isinstance(node, ast.Assign) and
                    node.targets[0].id == '__version__'):
                version = ast.literal_eval(node.value)
        if isinstance(version, tuple):
            version = '.'.join([str(x) for x in version])
        return version


install_requires = [
    'setuptools',
]
below35_requires = [
    'typing',
]
if 'bdist_wheel' not in sys.argv and sys.version_info < (3, 5):
    install_requires.extend(below35_requires)

tests_require = [
    'pytest >= 2.9.0',
    'import-order',
    'flake8',
]
docs_require = [
    'Sphinx',
]


setup(
    name='tsukkomi',
    version=get_version(),
    description='make tsukkomi for python types',
    long_description=readme(),
    url='https://github.com/spoqa/tsukkomi',
    author='Kang Hyojun',
    author_email='ed' '@' 'spoqa.com',
    license='Public Domain',
    packages=find_packages(exclude=['tests']),
    install_requires=install_requires,
    extras_require={
        ":python_version<'3.5'": below35_requires,
        'tests': tests_require,
        'docs': docs_require,
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
