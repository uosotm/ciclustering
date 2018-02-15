# CI Clustering

Ciclustering is an automation tool to collect, recognize and organize images for [Collective Idea](https://www.mikitotateisi.com/collective-idea/)

## Table of contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Documentation](#documentation)
    - [Arguments](#arguments)
    - [Options](#options)

## Requirements

- Python3.5 or above
- pip

## Installation

If you don't have Python3, it needs to be installed.

```
brew install python3
```

pip is also included in the installation.

Or if you want to install only pip, then:

```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
```

TODO: Add installation guide for ciclustering

## Documentation

```
Usage: ciclustering [OPTIONS] IMAGES_PATH

  CIclustering is an automation tool for Collective Idea

Options:
  --version    Display version.
  --dest TEXT  Path to output files.
  --help       Show this message and exit.
```

### Arguments

- IMAGES\_PATH: string  
    Path to directory that store input images.

### Options
 
- **keyword**: string  

- **dest**: string  
    Specify path to output files.  

- **version**:  
    Print version.

- **help**:  
    Show basic informations.
