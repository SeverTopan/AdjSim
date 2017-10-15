"""Setup"""

from setuptools import setup
import sys

if sys.version_info < (3,5):
    sys.exit('Python < 3.5 is not supported')

setup(name='adjsim',
      version='2.0.0',
      description='An Agent Based Modelling Engine tailored for Reinforcement Learning.',
      long_description=open('README.md', 'r').read(),
      url='https://github.com/SeverTopan/AdjSim',
      author='Sever Topan',
      packages=['adjsim'],
      license='GPL-3.0',
      classifiers = [
          'Development Status :: 3 - Alpha',

          'Intended Audience :: Developers',

          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'

          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
      ],
      keywords='agent based modelling ABM reinforcement learning',
      install_requires=['PyQt5', 'matplotlib', 'numpy'],
      python_requires='>=3.5, <3.7',
      )
