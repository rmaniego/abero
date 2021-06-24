"""
    Abero Runner
    (c) 2020 Rodney Maniego Jr.
    File analysis tool
"""

import os
import sys
import argparse

import abero

from arkivist import Arkivist


################
# abero logic  #
################
parser = argparse.ArgumentParser(prog="abero",
                                 description="Similarity analyzer.")
parser.add_argument("-d",
                    "--directory",
                    metavar="directory",
                    type=str,
                    help="Directory of the files.",
                    required=True)

parser.add_argument("-e",
                    "--extension",
                    metavar="extension",
                    type=str,
                    help="Allowed file extension to be analyzed.")

parser.add_argument("-c",
                    "--control",
                    metavar="control",
                    type=str,
                    help="Filepath of the control file.")

parser.add_argument("-t",
                    "--threshold",
                    metavar="threshold",
                    type=int,
                    help="Tolerance level for the analysis data.")

parser.add_argument("-u",
                    "--unzip",
                    metavar="unzip",
                    type=int,
                    help="Unzip flag")

parser.add_argument("-s",
                    "--skipnames",
                    metavar="skipnames",
                    type=int,
                    help="Skip files with common filenames.")

parser.add_argument("-g",
                    "--group",
                    metavar="group",
                    type=int,
                    help="Only compare when files has the same unique identifier.")

parser.add_argument("-r",
                    "--reset",
                    metavar="reset",
                    type=int,
                    help="Reset data before analyzing files.")

args = parser.parse_args()

# get submissions directory
directory = args.directory
if not abero.check_path(directory):
    print(f"\nAberoError: The directory was not found: {directory}")
    sys.exit(0)

extension = args.extension
if extension is None:
    extension = "txt"

# set the threshold level
threshold = abero.defaults(args.threshold, 1, 100, 80)

# get template path
template = args.control
if template is not None:
    if not abero.check_path(template):
        print(f"\nAberoWarning: File was not found: {template}")
        template = None

# set the skip names flag
skipnames = abero.defaults(args.skipnames, 0, 1, 0)

# set the group flag
group = abero.defaults(args.group, 0, 1, 0)

# set the unzip flag
unzip = abero.defaults(args.unzip, 0, 1, 0)

# set the clear data flag
reset = abero.defaults(args.reset, 0, 1, 0)

abero.analyze(directory, extension=extension, threshold=threshold, template=template, skipnames=skipnames, group=group, unzip=unzip, reset=reset)