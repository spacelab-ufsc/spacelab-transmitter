*********************
Packaging the Project
*********************

This page presents the instructions to packaging the source files of the project.

Generating an RPM package
=========================

To generate an RPM package, execute the command below:

::

    python setup.py bdist_rpm


If successful, the generated RPM package will be available in *dist/*.

Generating a DEB package
========================

To generate a DEB package, execute the steps below:

1. Prepare the source files with setuptools:

::

    python setup.py sdist


2. Generate the DEB package:

::

    ./build_deb_pkg.sh


If successful, the generated DEB package will be available in *scripts/*.

.. note::

   The current version of the build_deb_pkg.sh script was written to generate packages targeting Ubuntu 20.04! For other distros or Ubuntu versions, some modification inside the script are required.
