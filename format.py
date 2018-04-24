"""
Formats the cases text for easy reading.
(Remove double spacing, repetitive titles and html links)
Save each case as a separate txt file.
"""

import extract
import nltk as nl
import re

class Format:

    def pretty_case(self, case):
        """
        Cleans formating of pages in a case
        """
        clean = []
        for page in case:
            page = page.split("\n") # split on paragraphs
            for para in page:
                if para != "": # remove empty paragraphs
                    para = para.replace(" . . .", "")
                    clean += self.pretty_sentence(para)

        clean = self.pretty_head(clean)

        return clean

    def pretty_head(self, sentences):
        """
        Removes the headnote at the begining of a case
        """
        clean = []
        start = False
        for sent in sentences:
            judge = sent.split(" ")[0] #first word of a sentence

            if judge == "LORD" or judge == "LADY" or judge == "BARONESS": #NOTE might need more options for Lady Hale?
                start = True # flag to indicate start of the body proper
                clean.append("\n-------------NEW JUDGE---------------") # marking of a new judge
                clean.append(sent)

            elif start == True and sent != "": # remove empty sentences
                clean.append(sent)

        return clean

    def pretty_sentence(self, paragraph):
        """
        Cleans formating of sentences in a paragraph
        """
        clean = []
        sentences = nl.sent_tokenize(paragraph)
        for sent in sentences:
            sent = sent.lstrip() # removes chars from begining of a sentence
            sent = sent.replace("(back to preceding text)", "") # removes HTMl navigator link
            clean.append(sent)

        return clean

    def save(self, case, name, folder, link):
        """
        save the case as name.txt in /corpus
        """
        try:
            fname = "../corpus/" + folder + "/" + name + ".txt"
            file = open(fname, "w")
            self.write(case, file, link)
        except IOError:
            print("Courld not find the file: ", fname)

    def write(self, case, file, link):
        """
        write the case line by line in file
        """
        file.write(link + "\n")
        [file.write(line + "\n") for line in case]

if __name__ == "__main__":
    fm = Format()
    ex = extract.Extract()

    # Should write a cleanup case in the test folder
    case = []
    ex.extract_case("https://publications.parliament.uk/pa/ld199697/ldjudgmt/jd961121/smith01.htm", case)
    clean = fm.pretty_case(case)
    fm.save(clean, "1", "test")

    # Should catch error in file name and print it
    case = []
    ex.extract_case("https://publications.parliament.uk/pa/ld200809/ldjudgmt/jd090617/assom.htm", case)
    clean = fm.pretty_case(case)
    fm.save(clean, "2", "test2")
