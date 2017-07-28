#-------------------------------------------------------------------------------
# ADJECOSYSTEM SIMULATION FRAMEWORK
# Designed and developed by Sever Topan
#-------------------------------------------------------------------------------
from setuptools import setup
import sys

if sys.version_info < (3,5):
    sys.exit('Python < 3.5 is not supported')

setup(name='AdjSim',
      version='0.1.0',
      description='Ecosystem Simulation Framework',
      long_description=open('README.md', 'r').read(),
      author='Sever Topan',
      packages=['AdjSim'],
      license='GPL-3.0',
      install_requires=['matplotlib']
      )
