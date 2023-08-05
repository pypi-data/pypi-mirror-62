from setuptools import setup, Command, errors, find_packages
import sys
from shutil import rmtree
import os

VERSION = "0.0.5"

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()


class SetupCommand(Command):
    """Base class for setup.py commands with no arguments"""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def rmdir_if_exists(self, directory):
        self.status("Deleting {}".format(directory))
        rmtree(directory, ignore_errors=True)


def build():
    return os.system(
        "{executable} setup.py sdist bdist_wheel --universal".format(executable=sys.executable))


class BuildDistCommand(SetupCommand):
    """Support setup.py upload."""
    description = "Build the package."

    def run(self):
        self.status("Removing previous builds...")
        self.rmdir_if_exists(os.path.join(here, 'dist'))

        self.status("Building Source and Wheel (universal) distribution...")
        build()
        sys.exit()


class UploadCommand(SetupCommand):
    """Support setup.py upload."""
    description = "Build and publish the package."

    def run(self):

        self.status("Removing previous builds...")
        self.rmdir_if_exists(os.path.join(here, 'dist'))

        self.status("Building Source and Wheel (universal) distribution...")
        exit_code = build()
        if exit_code != 0:
            raise errors.DistutilsError("Build failed.")
        self.status("Uploading the package to PyPI via Twine...")
        os.system("twine upload dist/*")

        self.status("Pushing git tags...")
        os.system("git tag v{about}".format(about=VERSION))
        os.system("git push --tags")

        sys.exit()


setup(
    name="meeshkan-tutorial",
    version=VERSION,

    install_requires=["meeshkan>=0.2.13", "clint",
                      "pyfiglet", "progress", "http-types>=0.0.11"],
    packages=find_packages(exclude=('tests',)),
    # metadata to display on PyPI
    author="Meeshkan",
    author_email="mike@meeshkan.com",
    description="A tutorial for Meeshkan",
    keywords="meeshkan testing",
    url="https://github.com/meeshkan/meeshkan-tutorial",
    extras_require=dict(dev=['setuptools', 'twine', 'wheel']),
    entry_points={'console_scripts': ['meeshkan-tutorial = meeshkan_tutorial.tutorial:cli']},
    long_description=long_description,
    long_description_content_type='text/markdown',
    cmdclass={
        'dist': BuildDistCommand,
        'upload': UploadCommand
    }
)
