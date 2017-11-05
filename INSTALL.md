## Installing and Running AdjSim

### Set Up Virtual Environment

It is reccommended to run AdjSim using virtual python environments provided by Anaconda or Pip. The following describes the installation procedure for each of these.

Make sure Python 3.5 or 3.6 is installed, then create a new environment with it.

    # If using Virtualenv
    virtualenv --python=/usr/bin/python3.6 venv
    source venv/bin/activate

    # If using Anaconda
    conda create --name adjsim python=3.6
    activate adjsim

### Install Using Pip (Recommended)

Invoke pip. This works with either of the above virtual environments.

    pip install adjsim

### Install Using Anaconda

Invoke conda. This only works with an anaconda environment. Currently only available for Windows.

    conda install -c st7anaconda adjsim

### Install Using GitHub Repository

Clone the GitHub repository.

     git clone https://github.com/SeverTopan/AdjSim

Install Dependencies.

     python setup.py install

Note: If you run into trouble importing PyQt5 when installing using the setup.py file, try using

    pip install -e .