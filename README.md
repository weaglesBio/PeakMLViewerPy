## PeakMLViewerPy - Version 0.1.0

## Setting up release

Release consists of zipped folder PeakMLViewerPy_X_X_X.
Executable requires MoleculeDatabases folder and settings.xml file stored at same root, which is how the file is packaged.
Errors and user actions are written to .txt log file at root.

## Publishing project as executable

```
pyinstaller --onefile -w -F -i "favicon.ico" PeakMLViewerPy.py
```
