## AdjSim Release Workflow

This file details the release workflow for AdjSim for quick reference.

### 1. Update Config File Versions

Update all files withing AdjSim to display the new version. (setup.py, etc.)

### 2. Push Changes, Create New Github Release

Push changes to github, publish new release.

### 3. Publish to PyPI

In adjsim root directory:

    python setup.py sdist
    python setup.py bdist_wheel
    twine upload dist/*

### 4. Publish to Anaconda

In adjsim root directory:

    conda-build .
    conda convert --platform all <path/from/previous/command> -o build/
    anaconda upload <all previously created distributions>

### 5. Update Documentation

In the adjsim/docs directory:

    make html

Then copy generated files into the gh-pages branch.