import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand
from shpotipy.shpotipy import __version__


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


setup(
    name="shpotipy",
    version=__version__,
    description="A python based command line interface for Spotify.",
    author="Gabriele Bonetti",
    author_email="gabriele.bonetti@gmail.com",
    url="https://github.com/g-bon/shpotipy",
    install_requires=["docopt", "colored", "pyperclip", "requests"],
    license="MIT",
    zip_safe=False,
    keywords="shpotipy",
    packages=["shpotipy"],
    entry_points={"console_scripts": ["spotipy = shpotipy.shpotipy:main"]},
    tests_require=["pytest"],
    cmdclass={"test": PyTest},
)
