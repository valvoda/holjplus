"""
Formats the cases text for easy reading.
(Remove double spacing, repetitive titles and html links)
Save each case as a separate txt file.
"""

import extract
import nltk as nl
import re

class Format:

    # NOTE this needs to be simplified a lot!!!
    def prettify(self, case):
        """
        clean up the extracted html text to adhere to the HOLJ formating
        """
        clean1 = []
        for c in case:
            c = c.replace("(back to preceding text)", "") #remove html navigation text
            c = c.replace("  ", "") #remove double spaces
            c = c.split("\n") #remove breaklines
            clean1 += [i for i in c if i != ""]

        clean2 = []
        for c in clean1:
            sent = nl.sent_tokenize(c)
            for s in sent:
                s = s.lstrip()
                if re.search("\w", s) != None:
                    clean2.append(s)

        clean3 = []
        start = False
        for c in clean2:
            judge = c.split(" ")[0]
            if judge == "LORD" or judge == "LADY" or judge == "BARONESS": #NOTE might need more options for lady hale
                start = True
                clean3.append("\n-------------NEW JUDGE---------------")
            if start == True:
                clean3.append(c)

        return clean3

    def save(self, case, name, folder):
        """
        save the case as name.txt in /corpus
        write it line by line
        """
        file = open("../corpus/" + folder + "/" + name + ".txt", "w")

        for line in case:
            file.write(line + "\n")
        file.close()


if __name__ == "__main__":
    fm = Format()
    ex = extract.Extract()

    case = []
    ex.extract_case("https://publications.parliament.uk/pa/ld199697/ldjudgmt/jd961121/smith01.htm", case)
    clean = fm.prettify(case)
    fm.save(clean, "1")

    case = []
    ex.extract_case("https://publications.parliament.uk/pa/ld200809/ldjudgmt/jd090617/assom.htm", case)
    clean = fm.prettify(case)
    fm.save(clean, "2")
