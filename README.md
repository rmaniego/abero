![](/resources/banner.png)

# abero
Analyze multiple files for similarity and/or uniqueness.

## Requirements
- [Arkivist](https://pypi.org/project/arkivist/) `pip install arkivist`

## Lexicon
[W3Schools / Python](https://www.w3schools.com/python/)
[Python 3.9.5 Documentation](https://docs.python.org/3/download.html)
[first20hours / google-10000-english](https://github.com/first20hours/google-10000-english)
[Wikipedia Word Frequency](https://raw.githubusercontent.com/IlyaSemenov/wikipedia-word-frequency/master/results/enwiki-20190320-words-frequency.txt)

## Usage
```bash
# usage: abero [-h] -d directory [-e extension] [-c control] [-t threshold] [-u unzip] [-s skipnames] [-g group] [-r reset]

py abero.py -d "<path_to_files>" -e "txt" -c "<path_to_control_file>" -t 1 -u 1 -s 1 -r 1
```

**1.** `-d <path>` - Full path of the dirctory containing the files to analyze.
**1.** `-e <txt>` - List of allowed file extensions to analyze.
**2.** `-c <*.txt>` - Full path of the control file.
**3.** `-t <*.csv>` - Tolerance level for uniqueness (1-100; default = 0)
**4.** `-u <0>` - Unzip/extract ZIP files (0-1; default = 0)
**5.** `-s <0>` - Skip files with common names (0-1; default = 0)
**6.** `-g <0>` - Only compare if files contains the same identifier (0-1; default = 0)
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
