"""
Run to
Saves the HOLJ+ corpus in
../corpus/["09", "08", "07", "06", "05", "04", "03", "02", "01", "00", "99", "98", "97", "96"]
"""

import re
import format
import extract
import scrape
import os

class Holjplus:

    def __init__(self):
        self.ex = extract.Extract()
        self.sc = scrape.Scrape()
        self.fm = format.Format()
        self.name = 1 # The cases get a number for a name starting with 1
        self.allowed = ["09", "08", "07", "06", "05", "04", "03", "02", "01", "00", "99", "98", "97", "96"]

    def main(self):
        """
        Loops through all the links and saves cases and deletes misformated ones
        """
        html = self.sc.simple_get("https://publications.parliament.uk/pa/ld/ldjudgmt.htm") # open HOL website
        links = self.ex.extract_links(html) # find all links
        corpus = self.ex.filter_holinks(links) # keep and format only HOL links as a list

        for link in corpus:
            folder = self.get_folder(link)
            if folder != None:
                self.new_case(link, folder)

        self.clean_duplicates()

    def new_case(self, link, folder):
        """
        Saves a new case in appropriate folder and name
        """
        case = []

        if self.ex.extract_case(link, case, folder) != False:
            clean = self.fm.pretty_case(case)
            if clean:
                self.fm.save(clean, str(self.name), folder, link)
                self.name += 1
            # prints links with report formating
            else:
                print("Report: ", link)
        else:
            # prints inaccesible links
            print(link)

    def get_folder(self, link):
        """
        Separates cases by year of judgement
        """
        match = re.search("/jd(\d{2})", link)
        directory = match.group(1)

        if directory in self.allowed: #ignore misformated links
            return directory
        else:
            return None

    def clean_duplicates(self):
        """
        Removes cases with duplicated judgement
        """
        files = self.get_filenames()

        for file in files:
            f = open(file, "r")
            if self.check_duplicates(f) == True:
                os.remove(file)
                print("Removed: ", file)

    def get_filenames(self):
        """
        Navigates through directory to get all case paths
        """
        names = []

        directory = "../corpus"
        for filename in os.listdir(directory):
            if filename in self.allowed:
                for file in os.listdir(directory + "/" + filename):
                    if file.endswith(".txt"):
                        names.append(directory + "/" + filename + "/"+ file)

        return names

    def check_duplicates(self, file):
        """
        Checks if a case has two or more judgements from the same judge
        """
        content = file.readlines()
        content = [x.strip() for x in content]

        judges = []
        for i in range(len(content)):
            if content[i] == "-------------NEW JUDGE---------------":
                judges.append(content[i+1])
            i += 1

        if len(judges) != len(set(judges)):
            return True

        return False

if __name__ == '__main__':
    hj = Holjplus()
    hj.main()
