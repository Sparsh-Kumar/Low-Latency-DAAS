import setuptools
from os.path import join, dirname

dir: str = dirname(__file__)

long_description: str | None = None
package_requirements: str | None = None

with open(join(dir, 'README.md')) as readme:
  long_description = readme.read()

with open(join(dir, 'requirements.txt')) as requirements:
  package_requirements = requirements.read().splitlines()

setuptools.setup(
  name='lib_logger',
  description='Re-usable logger utility for the application.',
  long_description=long_description,
  long_description_content_type='text/markdown',
  url='',
  install_requires=package_requirements,
  packages=setuptools.find_packages()
)

