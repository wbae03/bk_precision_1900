# BK Precision 1900

## Description

This project implements the BK Precision 1902B control as a Python context manager. It allows users to easily access and manipulate the BK Precision 1902B control through a Python interface. It is only tested with the BK 1902B Power supply but should work with all of any supply for the 1900 series.

## Installation

### Via pip

To install the package from PyPI using pip, run the following command:

pip install bk_precision_1900

### From the repository

To install the package from the repository, clone the repository and install it using poetry:

```bash
git clone https://github.com/DephyInc/bk_precision_1900
cd bk_precision_1900
poetry install
```

## Running the Demo Code

To run the demo code, use the following command:

```bash
poetry run python bk_demo.py [SERIAL_PORT]
```

This will execute the `bk_demo.py` script, which sets a series of voltages in the BK Precision 1902B and prints out the display readouts.

Note that you will need to have poetry installed on your system in order to use the poetry run command. You can install poetry by following the instructions at https://python-poetry.org/docs/.
