Deployment
==========

If you wish to create a new version manually, the process is:

1. Update version info in ``setup.py``

1. Install the requirements in requirements_dev.txt

1. Set up a config file at ~/.pypirc

1. Generate a distribution

    ::

        python setup.py bdist

1. Upload the distribution

    ::

        twine upload dist/* -r pypi (or pypitest)

