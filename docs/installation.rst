************
Installation
************

Before using the SpaceLab Transmitter, ensure that you have the necessary dependencies installed, including Python 3, GTK 3, and the required Python libraries (e.g., `numpy`, `scipy`). All the required dependencies are listed below:

* `PyGObject <https://pypi.org/project/PyGObject/>`_
* `PyNGHam <https://pypi.org/project/pyngham/>`_
* `NumPy <https://pypi.org/project/numpy/>`_
* `SciPy <https://pypi.org/project/scipy/>`_
* `PyEphem <https://pypi.org/project/ephem/>`_
* `UHD <https://github.com/EttusResearch/uhd>`_
* `PyADI-IIO <https://github.com/analogdevicesinc/pyadi-iio>`_
* `PyModulation <https://pypi.org/project/pymodulation/>`_

Installing Adalm Pluto SDR driver and API
=========================================

For using the Adalm Pluto SDR, the following dependencies are required:

* **libiio**: Analog Device’s “cross-platform” library for interfacing hardware.
* **libad9361-iio**: AD9361 is the specific RF chip inside the PlutoSDR.
* **pyadi-iio**: Python API. It depends on the previous two libraries.

Unfortunatelly, for the installation of those libraries, manual compilation and installation must be performed. For that, the following step must be executed:

.. code-block:: bash

    sudo apt update
    sudo apt install build-essential git libxml2-dev bison flex libcdk5-dev cmake python3-pip libusb-1.0-0-dev libavahi-client-dev libavahi-common-dev libaio-dev
    cd ~
    git clone --branch v0.23 https://github.com/analogdevicesinc/libiio.git
    cd libiio
    mkdir build
    cd build
    cmake -DPYTHON_BINDINGS=ON ..
    make -j$(nproc)
    sudo make install
    sudo ldconfig

.. code-block:: bash

    cd ~
    git clone https://github.com/analogdevicesinc/libad9361-iio.git
    cd libad9361-iio
    mkdir build
    cd build
    cmake ..
    make -j$(nproc)
    sudo make install

.. code-block:: bash

    cd ~
    git clone --branch v0.0.14 https://github.com/analogdevicesinc/pyadi-iio.git
    cd pyadi-iio
    pip3 install -r requirements.txt
    sudo python3 setup.py install
