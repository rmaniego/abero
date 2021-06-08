"""
    (c) 2020 Rodney Maniego Jr.
    File analysis tool
"""

VERSION = "1.1.0"

print(f"\nAbero v{VERSION}")

print("\nLoading requirements...")
print("Please wait...")

import os
import re
import sys
import zipfile
import argparse

from arkivist import Arkivist
from statistics import mean

print("Done.")

def analyze(directory, threshold=80, template=None, skipnames=0, unzip=0, reset=0):

    # do not hard code
    extension = "py" # csv
    
    if not isinstance(directory, str):
        print("AberoError: 'directory' parameter must be a string.")
        return

    validate(threshold, 1, 100, 80)
    validate(skipnames, 0, 1, 0)
    validate(unzip, 0, 1, 0)
    validate(reset, 0, 1, 0)
    
    template_filename = ""
    if isinstance(template, str):
        if not check_path(template):
            print("AberoWarning: Template file was not found.")
            template = None
    
    if unzip == 1:
        print("\nUnzipping files:")
        if not check_path(f"{directory}"):
            os.makedirs(f"{directory}")
        for filename in get_filenames(directory, ["zip"]):
            print(f" - {filename}")
            extract(f"{directory}/{filename}", f"{directory}")

    print("\nAnalyzing files...")
    
    prev = ""
    if template is not None:
        template_filename = template.split("\\")[-1:][0]

    # extensions = extensions.split(",")
    analysis = Arkivist(f"{directory}/analysis.json")
    if reset == 1:
        analysis.clear()
    filenames = get_filenames(f"{directory}", [extension])
    for index, filename in enumerate(filenames):
        if template_filename != filename:
            codelines = {}
            filepath = f"{directory}/{filename}"
            for compare in filenames:
                uid = compare
                if template_filename == compare:
                    uid = "template"
                if filename != compare:
                    skip = False
                    if skipnames == 1:
                        common = common_string(filename, compare)
                        if common in compare:
                            if len(common) >= 15:
                                skip = True
                    if not skip:
                        result = similarity(filepath, f"{directory}/{compare}")
                        codelines.update({uid: result})
            
            metadata = analysis.get(filename, {})
            metadata.update({"codelines": codelines})
            analysis.set(filename, metadata)
    
    print("\nGenerating report...")
    count = 0
    analysis.reload()
    for filename, metadata in analysis.show().items():
        count += 1
        print(f"\n File #{count}: {filename}")
        codelines = metadata.get("codelines", {})
        control = codelines.get("control", {})
        control_avg = average(list(control.values()), threshold)
        duplicates = [0]
        for compare, result in codelines.items():
            if compare != "template":
                avg = average(list(result.values()), threshold)
                avg = avg - control_avg
                if avg > 0:
                    duplicates.append(avg)
                    print(f" - {avg:.2f}% {compare}")
        originality = (100 - max(duplicates))
        print(f" * Originality Rating: {originality:.2f}%")
        statistics = metadata.get("statistics", {})
        statistics.update({"originality": originality})
        metadata.update({"statistics": statistics})
        analysis.set(filename, metadata)

def average(results, threshold):
    if len(results) == 0:
        return 0
    values = []
    for value in results:
        rate = value.get("1", 0)
        if rate < threshold:
            rate = 0
        values.append(rate)
    return round(mean(values), 2)

def similarity(original, compare):
    """ Compare original file to other files """
    duplicates = {}
    data1, data2 = "", ""
    with open(original, "r") as file1:
        data1 = file1.read()
    with open(compare, "r") as file2:
        data2 = file2.read()
        
        
    
    for line1 in data1.split("\n"):
        rate = 0
        words1 = pad(line1).split(" ")
        words1 = [i for i in words1 if i.strip() != ""]
        # words1.sort()
        if len(set(words1)) > 0:
            line = ""
            for line2 in data2.split("\n"):
                words2 = pad(line2).split(" ")
                words2 = [i for i in words2 if i.strip() != ""]
                if len(set(words2)) > 0:
                    if line1.strip() == line2.strip():
                        rate = 100
                        line = line2
                    else:
                        diff1 = difference(words2, words1)
                        diff2 = difference(words1, words2)
                        words3 = []
                        words3.extend(words1)
                        words3.extend(words2)
                        remain = len(diff1) + len(diff2)
                        if remain == 0:
                            rate = 100
                            line = line2
                        else:
                            temp = ((len(words3) - remain) / len(words3)) * 100
                            if temp > rate:
                                rate = temp
                                line = line2
            duplicates.update({line1: {"0": line, "1": rate}})
    return duplicates

def pad(string):
    """ Decongest statements """
    padded = string.replace("\r", "").replace("\t", " ")
    symbols = ["#", "%", "*", ")", "+", "-", "=",
                "{", "}", "]", "\"", "'", "<", ">" ]
    for item in symbols:
        padded = padded.replace(item, f" {item} ")
    return padded.replace("(", "( ")

def difference(diff, words):
    
    paired = []
    diff = [i for i in diff]
    pairs = {"(": ")", "{": "}", "[": "]", "\"": "\"", "'": "'" }
    for item in words:
        if item in diff:
            if item in paired:
                paired.remove(item)
                diff.remove(item)
            else:
                if len(item) > 1 and item in diff:
                    diff.remove(item)
            for pair in pairs.keys():
                if pair in item and not ("\\\"" in item) and not ("\\\'" in item):
                    paired.append(pairs.get(pair, ""))
                    if item in diff:
                        diff.remove(item)
            else:
                if item in diff:
                    diff.remove(item)
    return diff

def validate(value, minimum, maximum, fallback):
    if not isinstance(value, int):
        print("KymeraWarning: Parameter must be an integer.")
        value = int(fallback)
    if not (minimum <= value <= maximum):
        print(f"KymeraWarning: Parameter must be an integer between {minimum}-{maximum}.")
        value = int(fallback)
    return value

def extract(path, destination):
    with zipfile.ZipFile(path, "r") as zip:
        zip.extractall(destination)

def common_string(original, compare):
    common = []
    limit = min((len(original), len(compare)))
    for i in range(0, limit):
        if original[i] != compare[i]:
            break
        common.append(original[i])
    # print("".join(common))
    return "".join(common)

def default(value, minimum, maximum, fallback):
    if value is not None:
        if not (minimum <= value <= maximum):
            return fallback
        return value
    return fallback

# file/folder io
def get_folders(source):
    return [f.name for f in os.scandir(source) if f.is_dir()]

def check_path(path):
    if path.strip() == "":
        return False
    return os.path.exists(path)

def get_filenames(path, extensions=[]):
    filenames = []
    for filepath in os.listdir(path):
        if filepath.split(".")[-1].lower() in extensions:
            filenames.append(filepath)
    return filenames


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

parser.add_argument("-r",
                    "--reset",
                    metavar="reset",
                    type=int,
                    help="Reset data before analyzing files.")

args = parser.parse_args()

# get submissions directory
directory = args.directory
if not check_path(directory):
    print(f"\nAberoError: The directory was not found: {directory}")
    sys.exit(0)

# set the threshold level
threshold = default(args.threshold, 1, 100, 80)

# get template path
template = args.control
if template is not None:
    if not check_path(template):
        print(f"\nAberoWarning: File was not found: {template}")
        template = None

# set the skip names flag
skipnames = default(args.skipnames, 0, 1, 0)

# set the unzip flag
unzip = default(args.unzip, 0, 1, 0)

# set the clear data flag
reset = default(args.reset, 0, 1, 0)

analyze(directory, threshold=threshold, template=template, skipnames=skipnames, unzip=unzip, reset=reset)