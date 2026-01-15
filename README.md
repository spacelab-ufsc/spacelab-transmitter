<h1 align="center">
    SPACELAB-TRANSMITTER
    <br>
</h1>

<h4 align="center">Packet transmitter of the SpaceLab's satellites.</h4>

<p align="center">
    <a href="https://github.com/spacelab-ufsc/spacelab-transmitter">
        <img src="https://img.shields.io/badge/status-development-green?style=for-the-badge">
    </a>
    <a href="https://github.com/spacelab-ufsc/spacelab-transmitter/releases">
        <img alt="GitHub commits since latest release (by date)" src="https://img.shields.io/github/commits-since/spacelab-ufsc/spacelab-transmitter/latest?style=for-the-badge"> 
    </a>
    <a href="https://github.com/spacelab-ufsc/spacelab-transmitter/blob/main/LICENSE">
        <img src="https://img.shields.io/badge/license-GPL3-yellow?style=for-the-badge">
    </a>
</p>

<p align="center">
    <a href="#overview">Overview</a> •
    <a href="#dependencies">Dependencies</a> •
    <a href="#installing">Installing</a> •
    <a href="#documentation">Documentation</a> •
    <a href="#license">License</a>
</p>

## Overview

SpaceLab Packet Transmitter is a software to transmit audio records to the satellites of SpaceLab.

Below, there is an image of the main window of the software:

<img src="docs/img/main-window.png" width=""/>

### Satellites

This program will support the satellites below:

* FloripaSat-1 (launched in December 2019)
* FloripaSat-2
* GOLDS-UFSC
* Catarina-A1
* Catarina-A2

## Dependencies

* [PyGObject](https://pypi.org/project/PyGObject/)
* [PyNGHam](https://pypi.org/project/pyngham/)
* [NumPy](https://pypi.org/project/numpy/)
* [SciPy](https://pypi.org/project/scipy/)
* [PyEphem](https://pypi.org/project/ephem/)
* [UHD](https://github.com/EttusResearch/uhd)
* [PyADI-IIO](https://github.com/analogdevicesinc/pyadi-iio)
* [ZeroMQ](https://zeromq.org/)
* [PyModulation](https://pypi.org/project/pymodulation/)

### Installation on Ubuntu

```sudo apt install python3 python3-gi python3-numpy python3-scipy python3-ephem python3-pyzmq python3-uhd```

```pip install pyngham pyadi-iio pymodulation```

### Installation on Fedora

```sudo dnf install python3 python3-gobject python3-numpy python3-scipy python3-ephem python3-pyzmq uhd uhd-devel```

```pip install pyngham pyadi-iio pymodulation```

## Installing

```python setup.py install```

## Documentation

The documentation of this project is generated using the Sphinx tool, and it is available [here](https://spacelab-ufsc.github.io/spacelab-transmitter/).

### Dependencies

* Sphinx
* sphinx-rtd-theme

### Building the Documentation

```make html```

## License

This project is licensed under GPLv3 license.
