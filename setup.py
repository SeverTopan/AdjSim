"""Setup"""

from setuptools import setup
import sys

setup(name='adjsim',
      version='2.0.1',
      description='An Agent Based Modelling Engine tailored for Reinforcement Learning.',
      long_description=open('README.rst', 'r').read(),
      url='https://github.com/SeverTopan/AdjSim',
      author='Sever Topan',
      packages=['adjsim'],
      license='GPL-3.0',
      classifiers = [
          'Development Status :: 3 - Alpha',

          'Intended Audience :: Developers',

          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
      ],
      keywords='agent based modelling ABM reinforcement learning',
      install_requires=['PyQt5==5.9', 'matplotlib==2.0', 'numpy==1.13'],
      python_requires='>=3.5, <3.7',
      )
