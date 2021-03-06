from setuptools import setup, find_packages
from pip._internal.req import parse_requirements

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements("requirements.txt", session=False)

# reqs is a list of requirement
try:
	reqs = [str(ir.req) for ir in install_reqs if ir.req is not None]
except:
	reqs = [str(ir.requirement) for ir in install_reqs if ir.requirement is not None]

setup(name='referralmanager',
      version='0.1.0',
      packages=find_packages(exclude=('tests*', 'docs', 'examples')),
      install_requires=reqs,
      entry_points={
          'console_scripts': [
              'refman = referralmanager.cli.base:base'
          ]
      }
      )
