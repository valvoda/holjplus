"""
Allows for selecting the size of the corpus and merging it with existing case
collections. ie. the original HOLJ corpus
- https://www.inf.ed.ac.uk/research/isdd/admin/package?download=84
"""

import os
import filecmp
import re
from shutil import copyfile
import random
import pickle

class Merge:

    def check_duplicates(self, path):
        """
        Checks the created files for duplicatesself.
        Prints Error and their names if it finds some.
        """
        for i in os.listdir(path):
            for j in os.listdir(path):
                if i != j: #ignore when same file
                    if filecmp.cmp(path + "/" + i, path + "/" + j):
                        print("ERROR", i, j)

        print("Done")

    def merge_corpus(self, newpath, old, max, destination):

        new = self.get_corpus(newpath)
        name = 1 #name files from 1 to N
        max = max - len(old) #find

        for file in old: #copy all the oldcorpus files
            copyfile(file, destination + "/" + str(name) + ".txt")
            name += 1

        total = []
        while len(total) != max:
            i = random.randint(0, len(new))
            if (not new[i] in old) and (i not in total):
                total.append(i)

        for t in total:
            copyfile(new[t], destination + "/" + str(name) + ".txt")
            name += 1

    def find_old(self, newpath, oldpath):
        """ finds all the old cases in the new corpus """
        oldCorp = []
        new = self.get_corpus(newpath)
        old = self.get_corpus(oldpath)
        old.sort(key=lambda x: int(re.findall("\d+", x)[0])) # Keep the order

        for caseA in old:
            wordsA = self.format_spaces(caseA)
            maxNum = 0
            maxName = None
            for caseB in new:
                wordsB = self.format_spaces(caseB)
                same = list(set(wordsA).intersection(wordsB))
                if maxNum < len(same): # Finds the most similar case
                    maxName = caseB
                    maxNum = len(same)
            print(maxName + ": ", maxNum) #Print old corpus content in new corpus
            oldCorp.append(maxName)

        return oldCorp

    def format_spaces(self, case):
        """ Unifies line formating """
        lines = self.get_content(case)
        words = []
        for line in lines:
            words.append(re.sub(" ", "", line))

        return words

    def get_corpus(self, path):
        """
        Open coropus and get all the paths to a file.
        Works with /corpus/O1/file.txt
        and /corpus/file.txt
        """
        corpus = []

        for filename in os.listdir(path):
            if filename.isdigit():
                for case in os.listdir(path + "/" + filename):
                    if case.endswith(".txt"):
                        corpus.append(path + "/" + filename + "/" + case)
            elif filename.endswith(".txt"): #for /corpus/file.txt
                corpus.append(path + "/" + filename)

        return corpus

    def get_content(self, file):
        """ Gets all the lines of a file """
        case = open(file, "r")
        content = case.readlines()
        content = [x.strip() for x in content]

        return content

    def save_corpus(self, files):
        """ Saves corpus """
        with open('save.p', 'wb') as handle:
            pickle.dump(files, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def load_corpus(self):
        """ Loads corpus """
        with open('save.p', 'rb') as handle:
            files = pickle.load(handle)
        return files

    def main(self):
        """
        newpath for new corpus
        oldpath for old corpus
        destination for merged corpus
        max for total in merged corpus
        first if no saved old corpus
        """
        newpath = "../corpus"
        oldpath = "../ogcorpus"
        destination = "../selection"
        max = 300
        first = False

        if first: #pickle results as comparing files takes long time
            print("Finding Old")
            old = self.find_old(newpath, oldpath)
            self.save_corpus(old)
            print("Found Old")
        else:
            old = self.load_corpus()

        self.merge_corpus(newpath, old, max, destination)
        self.check_duplicates(destination)

if __name__ == '__main__':
    mer = Merge()
    mer.main()
