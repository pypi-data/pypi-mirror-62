try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

tests_require = ['pytest', 'Sphinx']

long_description = """
Curio is a coroutine-based library for concurrent systems programming.
"""


setup(name="curio",
      description="Curio",
      long_description=long_description,
      license="BSD",
      version="1.1",
      author="David Beazley",
      author_email="dave@dabeaz.com",
      maintainer="David Beazley",
      maintainer_email="dave@dabeaz.com",
      url="https://github.com/dabeaz/curio",
      packages=['curio'],
      tests_require=tests_require,
      extras_require={
          'test': tests_require,
      },
      classifiers=[
          'Programming Language :: Python :: 3',
      ])
