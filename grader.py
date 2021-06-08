"""
    (c) 2020 Rodney Maniego Jr.
    Abero Grader
"""

VERSION = "1.0.0"

print(f"\nAbero Grader v{VERSION}")

print("\nLoading requirements...")
print("Please wait...")

import os
import re
import sys
import argparse

from arkivist import Arkivist

print("Done.")

# utils
def default(value, minimum, maximum, fallback):
    if value is not None:
        if not (minimum <= value <= maximum):
            return fallback
        return value
    return fallback

def get_float(label, minimum, maximum, fallback):
    try:
        query = input(label).strip()
        if query == "":
            return ""
        return default(float(query), minimum, maximum, fallback)
    except:
        return get_float(label)

def check_path(path):
    if path.strip() == "":
        return False
    return os.path.exists(path)

################
# abero logic #
################
parser = argparse.ArgumentParser(prog="abero",
                                 description="Similarity analyzer.")
parser.add_argument("-d",
                    "--directory",
                    metavar="directory",
                    type=str,
                    help="Directory of the files.",
                    required=True)

args = parser.parse_args()

# get submissions directory
directory = args.directory
if not check_path(directory):
    print(f"\nAberoError: The directory was not found: {directory}")
    sys.exit(0)

grading = Arkivist(f"{directory}/grading.json", sort=True)
for index, filename in enumerate(Arkivist(f"{directory}/analysis.json").keys()):
    count = index + 1
    userdata = grading.get(filename, {})
    grade = userdata.get("grade", 0)
    print(f"\nFile #{count} - {filename}")
    print(f" - Current grade: {grade}")
    grade = get_float(" - Set grade: ", 0, 100, 0)
    if grade != "":
        userdata.update({"grade": round(grade)})
        grading.set(filename, userdata)
    
