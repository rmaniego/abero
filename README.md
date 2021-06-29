![](/resources/banner.png)

# runner
Analyze multiple files for similarity and/or uniqueness.
Finding similarities of works duplicated from one or more part of different works to create a seemingly unique one can be difficult because of different strategies being used, but this can be done better with a software like runner.

## Requirements
- [Arkivist](https://pypi.org/project/arkivist/) `pip install arkivist`

## Usage
Install the latest abero package, upcoming versions might introduce unannounced changes, so a virtual environment is a must have before installation.
```bash
pip install -U abero
```

To integrate abero into your Python codes, check the code snippet below:
```python
import abero

abero.analyze(directory, extension="txt", threshold=80, template=None, skipnames=0, group=0, unzip=0, reset=0)
```

## CLI Usage
```bash
# usage: runner [-h] -d directory [-e extension] [-c control] [-t threshold] [-u unzip] [-s skipnames] [-g group] [-r reset]

py runner.py -d "<path_to_files>" -e "txt" -c "<path_to_control_file>" -t 1 -u 1 -s 1 -r 1
```

**1.** `-d <path>` - Full path of the dirctory containing the files to analyze.
**1.** `-e <txt>` - List of allowed file extensions to analyze.
**2.** `-c <*.txt>` - Full path of the control file.
**3.** `-t <*.csv>` - Tolerance level for uniqueness (1-100; default = 0)
**4.** `-u <0>` - Unzip/extract ZIP files (0-1; default = 0)
**5.** `-s <0>` - Skip files with common names (0-1; default = 0)
**6.** `-g <1>` - Only compare if files contains the same identifier (0-1; default = 1)
&emsp; **Example:** student1`_set1`.py >> student2`_set1`.py
**7.** `-r <0>` - Reset analytics before execution (0-1; default = 0)

## Control File
Control file contains words or phrases, checked line-by-line, that are deem allowed to be contained in all files to analyzed; therefore, if found on the test files, it will not be flagged as duplicate work.

## Features
- [x] Unzip feature
- [x] File comparison 
- [x] Threshold levels
- [x] Skip / group compare
- [ ] Diff tool, content viewer

## Did you know?
The repository name `runner` was inspired from the words aberrant and runner (Latin), which may mean deviating or being absent.
