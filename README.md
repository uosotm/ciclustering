# CI Clustering

Ciclustering is an automation tool to collect, recognize and organize images for [Collective Idea](https://www.mikitotateisi.com/collective-idea/)

## Table of contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Documentation](#documentation)
    - [Basic Usage](#basic-usage)
    - [Arguments](#arguments)
    - [Options](#options)
    - [Config file](#config-file)

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

  CI clustering is an automation tool for Collective Idea

Options:
  --version              Print version.
  --config TEXT          Path to config file.
  --dest TEXT            Path to output files.
  --mode [object|human]  Specify recognition mode
  --help                 Show this message and exit.
```

### Basic Usage

For instance, we have a directory like this:

```
.
├── accordion.jpg
├── bass.jpg
├── brain.jpg
├── camera.jpg
├── chair.jpg
├── cup.jpg
├── grand_piano.jpg
├── laptop.jpg
├── pizza.jpg
└── watch.jpg
```

To organize images by object recognition, then please run the following command.  
*Note: If you don't have a config file, the CLI prompts to create it.*

```
ciclustering .
```

You will be asked to specify a keyword for object recognition.

```
Please enter a keyward: cup
```

The process accepts only `.jpg` files.  
After running the command, `dest` direcotry should be created to store output files.

```
.
└── dest
    ├── cup
    │   └── cup.jpg
    ├── others
    │   ├── accordion.jpg
    │   ├── bass.jpg
    │   ├── brain.jpg
    │   ├── camera.jpg
    │   ├── chair.jpg
    │   ├── grand_piano.jpg
    │   ├── laptop.jpg
    │   ├── pizza.jpg
    │   └── watch.jpg
    └── results.csv
```

`results.csv` has a summary of recognition like `ImageFile, ObjectName1(score), ObjectName2(score)...`. Each lines of csv file are populated as a variable length record.

### Arguments

- IMAGES\_PATH: string  
    Path to directory that store input images.

### Options

- **config**: string (`~/.ciclustering` by default)  
    Specify path to config file.  

- **dest**: string (`./dest` by default)  
    Specify path to output files.  
    
- **mode**: chose `object` or `human` (`object` by default)  
    Indicate recognition mode.  *human mode* is not supported currently.  

- **version**:  
    Print version.

- **help**:  
    Show basic informations.

### Config file

Ciclustering uses config file to get some values to access Compute Vision API. The config file looks like below:

```
[default]
cva_url = https://vision.googleapis.com/v1/images:annotate
cva_key = <YOUR GCP API KEY>
```

The command attempts to read from `~/.ciclustering` by default. If there is no file there, it prompts you whether create a config or not.

```bash
Couldn't find (/Users/<YOUR USER NAME>/.ciclustering) to get config.
Would you like to create a new config there? [y/N]: y

Requests to [https://vision.googleapis.com/v1/images:annotate]:  # enter with empty to use default
Please enter your API KEY: <YOUR GCP API KEY>
```

You can also specify the custom path to config file.

```
ciclustering path/to/images --config path/to/config
```
