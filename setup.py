"""Setup"""

from setuptools import setup
import sys

if sys.version_info < (3,5):
    sys.exit('Python < 3.5 is not supported')

setup(name='adjsim',
      version='2.0.0',
      description='A clever agent based modelling engine',
      long_description=open('README.md', 'r').read(),
      author='Sever Topan',
      packages=['adjsim'],
      license='GPL-3.0',
      install_requires=['PyQt5', 'matplotlib', 'numpy']
      )
