import format
import extract
import scrape
import re

class Holjplus:

    def main(self):
        ex = extract.Extract()
        sc = scrape.Scrape()
        fm = format.Format()

        html = sc.simple_get("https://publications.parliament.uk/pa/ld/ldjudgmt.htm") # open website
        links = ex.extract_links(html) # find all links
        corpus = ex.filter_holinks(links) # keep and format only HOL links

        name = 1
        corpus = [corpus[126]]
        for link in corpus:
            print(link)
            match = re.search("/jd(\d{2})", link)
            directory= match.group(1)

            case = []
            if ex.extract_case(link, case) != False:
                clean = fm.prettify(case)
                if clean:
                    fm.save(clean, str(name), directory)
                    name += 1
                else:
                    print("Report: ", link)
            else:
                print(link)

if __name__ == '__main__':
    hj = Holjplus()
    hj.main()
