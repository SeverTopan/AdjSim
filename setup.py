from setuptools import setup

setup(name='AdjEcosystem',
      version='0.1',
      description='Ecosystem Simulation Framework'
      long_description=open('README.rst').read()
      author='Sever Topan'
      packages=['AdjEcosystem'],
      entry_points={
          'console_scripts': [
              'AdjEcosystem = AdjEcosystem.__main__:main'
          ]
      },
      )
