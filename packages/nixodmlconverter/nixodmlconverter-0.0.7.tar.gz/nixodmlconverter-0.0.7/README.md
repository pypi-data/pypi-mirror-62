[![Travis build](https://travis-ci.org/G-Node/nix-odML-converter.svg?branch=master)](https://travis-ci.org/G-Node/nix-odML-converter/)
[![Build status](https://ci.appveyor.com/api/projects/status/fc30meltvawsbpgt?svg=true)](https://ci.appveyor.com/project/G-Node/nix-odml-converter)
[![PyPI version](https://img.shields.io/pypi/v/nixodmlconverter.svg)](https://pypi.org/project/nixodmlconverter/)


# odML ↔️ NIX metadata conversion tool

This tool reads in [odML](https://g-node.github.io/python-odml/) / 
[NIX](https://g-node.github.io/nix/) files and writes the metadata structure to newly 
created NIX / odML files. When run as a script from the command line, it prints 
information regarding the number of Sections and Properties that were read, written, 
or skipped for various reasons.

For more information on the odML and NIX data formats, please check the sections below.

## Installation

You can easily install the converter via the Python package manager `pip`.

    pip install nixodmlconverter

## Usage

After installing the package, you can use the `convert.py` script found in the
directory 'nix-odML-converter/nixodmlconverter' that acts as a command line tool.

You can use it to a) import the content of an existing odML file into a NIX file or
b) to export the odML content of a NIX file into a new odML file. 

### Import of odML into a NIX file

From the command line use the `convert.py` script to import the contents of an existing
odML file into a NIX file:

    python nix-odML-convert/nixodmlconverter/convert.py odmlfile.xml nixfile.nix  

The odML file has to be provided in XML format. 

### Export odML from a NIX file

From the command line use the `convert.py` script to export the contents of an existing 
NIX file to a new odML file:

    python nix-odML-convert/nixodmlconverter/convert.py nixfile.nix newodmlfile.xml

### Usage notes

For compatibility with the NIX metadata format, which differs slightly from the 
odML format, the following modifications occur when converting from odML to NIX:

- If a Section has a `reference` create a property called `reference`
- If a Property has a `reference` put the reference in the Property's values
- Values of type `URL`, `person`, and `text` are treated as strings
- Values of type `datetime`, `date`, and `time` are converted to string representations
- Values of type `binary` are discarded


## Building from source

You can also install the package by cloning the github repository and
installing from source.

    git clone https://github.com/G-Node/nix-odML-converter.git
    cd nix-odML-converter
    python setup.py install

## Dependencies

* Python 3.6+
* Python packages:
    * odml (>=1.4.5)
    * nixio (>=1.5.0b3)

These dependency packages can be manually installed via the python package manager `pip`:

`pip install "odml>=1.4.5" "nixio>=1.5.0b3"` 

or by manually installing the nix-odML-converter from the repository root:

`python setup.py install`

Python 2 has reached end of life. Future versions of nixodmlconverter will no longer support Python 2.  We further recommend using a Python version >= 3.6.


# NIX (Neuroscience information exchange) format

The NIX data model allows to store fully annotated scientific datasets, i.e. the 
data together with its metadata within the same container. Our aim is to achieve 
standardization by providing a common/generic data structure for a multitude of 
data types.

The source code of the core python library is freely available on 
[GitHub](https://github.com/G-Node/nixpy) and can be installed via the 
Python package manager `pip` by typing `pip install nixio`.

More information about the project including related projects as well as tutorials and
examples can be found at our odML [project page](https://g-node.github.io/nix/).


# odML (Open metaData Markup Language) format

The open metadata Markup Language is a file based format (XML, JSON, YAML) for storing
metadata in an organised human- and machine-readable way. odML is an initiative to define
and establish an open, flexible, and easy-to-use format to transport metadata.

The source code of the core library is freely available on 
[GitHub](https://github.com/G-Node/python-odml) and can be installed via the 
Python package manager `pip` by typing `pip install odml`.

More information about the project including related projects as well as tutorials and
examples can be found at our odML [project page](https://g-node.github.io/python-odml/).
