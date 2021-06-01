"""
    (c) 2020 Rodney Maniego Jr.
    File analysis tool
"""

print(" Loading requirements...")
print(" Please wait...")

import os
import re

from arkivist import Arkivist
from statistics import mean

print(" Done.")

def analyze(folder="", extensions="", threshold=80, control_file="control_file"):
    # initialize data folder
    if not os.path.exists("data"):
        os.makedirs("data")

    # if folder is not set,
    # ask for folder inside the data directory
    folder = input("\n Folder name: ").strip()
    if folder not in get_folders("data"):
        print("Error: The folder was not found.")
        return

    # do not hard code
    extensions = "py" # csv
    
    if not isinstance(folder, str):
        print("AberoError: 'folder' parameter must be a string.")
        return
    
    if not isinstance(folder, str):
        print("AberoError: 'extensions' parameter must be a string.")
        return

    if not isinstance(threshold, int):
        print("AberoWarning: 'threshold' parameter must be an integer.")
        threshold = 80
    if not (1 <= threshold <= 100):
        print("AberoWarning: 'threshold' parameter must be an integer between 1-100.")
        threshold = 80
    
    if not isinstance(control_file, str):
        print("AberoWarning: 'control_file' parameter must be a string.")
        threshold = 80
    
    
    prev = ""
    extensions = extensions.split(",")
    analysis = Arkivist(f"data/{folder}/analysis.json")
    filenames = get_filenames(f"data/{folder}", extensions)
    for index, filename in enumerate(filenames):
        if control_file not in filename:
            count = index + 1
            print(f"\n File #{count}: {filename}")
            filepath = f"data/{folder}/{filename}"
            data = {}
            # save contents
            # contents = read_file(filepath)
            # code_lines = len(set(contents.split("\n")))
            for compare in filenames:
                uid = compare
                if control_file in compare:
                    uid = "control"
                if filename != compare:
                    result = similarity(filepath, f"data/{folder}/{compare}")
                    data.update({uid: result})
                    values = []
                    for value in result.values():
                        rate = value.get("1", 0)
                        if rate < threshold:
                            rate = 0
                        values.append(rate)
                    avg = round(mean(values), 2)
                    if avg > 0 and uid != "control":
                        print(f" - {avg:.2f}% {compare}")
        analysis.set(uid, data)

def word_frequency(contents):
    frequency = {}
    for line in contents.split("\n"):
        words = re.sub(r"[^A-Za-z0-9 _]+", " ", line).split(" ")
        count = [words.count(p) for p in words]
        for word, count in dict(list(zip(words,count))).items():
            sum = frequency.get(word, 0) + count
            frequency.update({word: sum})
    return frequency

def similarity(original, compare):
    duplicates = {}
    data1, data2 = "", ""
    with open(original, "r") as file1:
        data1 = pad(file1.read())
    with open(compare, "r") as file2:
        data2 = pad(file2.read())
    
    for line1 in data1.split("\n"):
        rate = 0
        words1 = line1.split(" ")
        words1 = [i for i in words1 if i.strip() != ""]
        # words1.sort()
        if len(set(words1)) > 0:
            line = ""
            for line2 in data2.split("\n"):
                words2 = line2.split(" ")
                words2 = [i for i in words2 if i.strip() != ""]
                if len(set(words2)) > 0:
                    diff1 = difference(words1, words2)
                    diff2 = difference(words2, words1)
                    words3 = []
                    words3.extend(words1)
                    words3.extend(words2)
                    remain = len(diff1) + len(diff2)
                    if remain == 0:
                        rate = 100
                    else:
                        temp = ((len(words3) - remain) / len(words3)) * 100
                        if temp > rate:
                            rate = temp
                            line = line2
            duplicates.update({line1: {"0": line, "1": rate}})
    return duplicates

def pad(string):
    padded = string.replace("\r", "").replace("\t", " ")
    symbols = [ "#", "%", "*", ")", "+", "-", "=",
                "{", "}", "]", "\"", "'", "<", ">" ]
    for item in symbols:
        padded = padded.replace(item, f" {item} ")
    return padded

def difference(words, diff):
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

# file/folder io
def read_file(filepath):
    try:
        with open(filepath, "r") as file:
            return file.read()
    except:
        return ""

def get_folders(source):
    return [f.name for f in os.scandir(source) if f.is_dir()]

def get_filenames(path, extensions=[]):
    filenames = []
    for filepath in os.listdir(path):
        if filepath.split(".")[-1].lower() in extensions:
            filenames.append(filepath)
    return filenames

def file_exists(filepath):
    return os.path.exists(filepath)


if __name__ == '__main__':
    analyze()