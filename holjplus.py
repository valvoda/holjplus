import re
import format
import extract
import scrape

class Holjplus:

    def __init__(self):
        self.ex = extract.Extract()
        self.sc = scrape.Scrape()
        self.fm = format.Format()
        self.name = 1 # The cases get a number for a name starting with 1

    def main(self):
        """
        This needs a cleanup.
        """

        html = self.sc.simple_get("https://publications.parliament.uk/pa/ld/ldjudgmt.htm") # open HOL website
        links = self.ex.extract_links(html) # find all links
        corpus = self.ex.filter_holinks(links) # keep and format only HOL links as a list

        for link in corpus:
            folder = self.get_folder(link)
            if folder != None:
                self.new_case(link, folder)

    def new_case(self, link, folder):
        case = []

        if self.ex.extract_case(link, case) != False:
            clean = self.fm.pretty_case(case)
            if clean:
                self.fm.save(clean, str(self.name), folder)
                self.name += 1
            # prints links with report formating
            else:
                print("Report: ", link)
        else:
            # prints inaccesible links
            print(link)

    def get_folder(self, link):
        match = re.search("/jd(\d{2})", link)
        directory = match.group(1)
        allowed = ["09", "08", "07", "06", "05", "04", "03", "02", "01", "00", "99", "98", "97", "96"]
        if directory in allowed: #ignore misformated links
            return directory
        else:
            return None

if __name__ == '__main__':
    hj = Holjplus()
    hj.main()
