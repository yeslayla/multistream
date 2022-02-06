
import re 
from os import path

from setuptools import setup
from codecs import open

app_name="multistream"
app_package="multistream"
app_requirements=["requests", "crossplane", "pyyaml"]

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

def read(*parts):
    return open(path.join(here, *parts), 'r').read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^version = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(
    name=app_name,
    version=find_version(app_package,'__init__.py'),
    description='Python application',
    long_description=long_description,
    long_description_content_type="text/markdown",

    # The project's main homepage.
    url='https://github.com/meteoritesolutions/multistream',

    # Author details
    author='Meteorite Online Solutions, LLC',
    author_email='engineering@meteoritesolutions.com',

    # Choose your license
    license='Proprietary',

    # See https://pypi.org/classifiers/
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Programming Language :: Python :: 3.9'
    ],
    keywords='Python',
    packages=[app_package],
    install_requires=app_requirements,
    package_data={},
    entry_points={
        'console_scripts' : [
            f"{app_name}={app_package}:cli"
        ]
    }
)