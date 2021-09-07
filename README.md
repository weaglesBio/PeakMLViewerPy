## PeakMLViewerPy - Version 0.2.0
***
## Setting up release

% Script/guide - set up environment to run locally

Release consists of zipped folder PeakMLViewerPy_X_X_X.

Current releases is for Windows 10 v2004 64-bit.
Pending release for MacOS Catalina.
Pending release for Linux Ubuntu v20.04.

Executable requires MoleculeDatabases folder and settings.xml file stored at same root, which is how the files are packaged.

Errors and user actions are written to .txt log file at root.
***
## Required Python libraries to run
- rdata
- ttkwidgets
- image
- lxml
- faker
- pyreadr
- scipy
***
## Compiling from source (Windows)

1. Install latest version of miniconda.
2. Run the following:
```
mkdir Source
cd Source
sudo apt install git
git clone https://github.com/weaglesBio/MetabolomicModellingMSc
cd MetabolomicModellingMSc

# Set up virtual environment to install libraries (required for rdkit)

conda create -c conda-forge -n peakml_env rdkit
conda activate peakml_env
pip install rdata
pip install ttkwidgets
pip install image
pip install lxml
pip install faker
pip install pyreadr
pip install scipy
pip install pyinstaller

pyinstaller PeakMLViewerPy_oswin.spec
```

Executable file available in dist folder.
***
## Compiling from source (macOS)

1. Install latest version of miniconda.
2. Run the following to initialise miniconda.
```
    source anaconda3/bin/activate
    conda init zsh
    conda init
```

2. Run the following as bash script in location for install:
```
# Download the source using git
mkdir Source
cd Source

# Installs XCode to install git if not installed
git --version 

git clone https://github.com/weaglesBio/MetabolomicModellingMSc
cd MetabolomicModellingMSc

# Set up virtual environment to install libraries (required for rdkit)

conda create -c conda-forge -n peakml_env rdkit
conda activate peakml_env
pip install rdata
pip install ttkwidgets
pip install image
pip install lxml
pip install faker
pip install pyreadr
pip install scipy
pip install pyinstaller

pyinstaller PeakMLViewerPy_osmac.spec
```

Executable file available in dist folder.
***
## Compiling from source (Linux)

1. Install latest version of miniconda.
2. Run the following as bash script in location for install:
```
mkdir Source
cd Source
sudo apt install git
git clone https://github.com/weaglesBio/MetabolomicModellingMSc
cd MetabolomicModellingMSc

sudo apt-get update -y
sudo apt-get install -y binutils-common

# Set up virtual environment to install libraries (required for rdkit)

conda create -c conda-forge -n peakml_env rdkit
conda activate peakml_env
pip install rdata
pip install ttkwidgets
pip install image
pip install lxml
pip install faker
pip install pyreadr
pip install scipy
pip install pyinstaller

pyinstaller PeakMLViewerPy_oslinux.spec
```

Binary file available in dist folder. Run with:
```
./PeakMLViewerPy
```
***
## Using IPA integration
%Include script for the IPA integration running in the GitHub.
