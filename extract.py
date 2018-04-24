"""
Extracts links to all cases.
Extracts text from cases.
Navigates through cases spanning several HTML sites.
"""

from bs4 import BeautifulSoup as bs
import scrape
import re
import six

class Extract:

    def extract_links(self, htmlfile):
        """
        Used to extract all the html links to cases from HOL website.
        """
        if htmlfile != None: #Check if valid file
            html = bs(htmlfile, 'html.parser')

        links = html.find_all('a') #Get all links
        links = [link.get("href") for link in links if isinstance(link.get("href"), six.string_types)] #Keep only the URl discard non-strings

        return links

    def filter_holinks(self, links):
        """
        Keep only links pointing to cases.
        """
        web = "https://publications.parliament.uk"
        links = [link for link in links if re.match(".+ld\d{6}.+",link)] #find hol links using regex

        hol = []
        for link in links: # normalize the links (some start with .. others with /pa)
            if link[:2] == "..":
                hol.append(web + "/pa" + link[2:])
            else:
                hol.append(web + link)

        return hol

    def extract_body(self, htmlfile):
        """
        Extracts the body of a judgement.
        """
        if htmlfile != None: #Check if valid file
            html = bs(htmlfile, "html5lib") # NOTE the standard html.parser does not work here!!!
        else:
            print("ERROR: could not get html!")
            return None, None

        # print(html.prettify()) #visualise the html

        end = html.find("a", string="continue")
        if end == None:
            end = html.find("a", string="Continue")

        if end != None:
            end = end.getText()

        text = html.find_all('tbody')
        text = [t.text for t in text]

        text = text[1:-1] # removes the webpage border around the body of the case

        return text, end

    def next_html(self, html):
        """
        Finds the link to the next part of a case.
        """
        num = re.search("(\d).htm", html) #find the number # NOTE what about 01, 02...10 notation?
        num = int(num.group(1)) + 1 #increse it by one
        html = re.sub("(\d).htm", str(num) + ".htm", html) #pass it back in

        return html

    def extract_case(self, html, all):
        """
        Extracts all the judgements from the case.
        Returns false if case is not accessible.
        """
        sc = scrape.Scrape()
        raw_html = sc.simple_get(html)
        text, end = self.extract_body(raw_html)

        if text == None:
            return False
        else:
            all += text

        if end is not None:
            html = self.next_html(html)
            self.extract_case(html, all)

if __name__ == "__main__":
    ex = Extract()
    sc = scrape.Scrape()

    error1 = "ERROR: Wrong number of links."
    error2 = "ERROR: Wrong links."

    print("Testing Extract:")

    # # Testing extraction of links
    # raw_html = sc.simple_get("https://publications.parliament.uk/pa/ld/ldjudgmt.htm")
    # links = ex.extract_links(raw_html)
    # assert (len(links) == 835), error1
    # assert (links[-1] == "http://www.parliament.uk/site-information/copyright/"), error2
    #
    # # Testing filtering of links
    # hol = ex.filter_holinks(links)
    # assert (len(hol) == 788), error1
    # assert (hol[0] == "https://publications.parliament.uk/pa/ld200809/ldjudgmt/jd090617/assom.htm"), error2
    # assert (hol[-1] == "https://publications.parliament.uk/pa/ld199697/ldjudgmt/jd961121/smith01.htm"), error2
    #
    # assert ex.next_html("https://publications.parliament.uk/pa/ld200809/ldjudgmt/jd090617/attgen-1.htm") \
    #  == "https://publications.parliament.uk/pa/ld200809/ldjudgmt/jd090617/attgen-2.htm", "ERROR, HTML does not increase."
    #
    # print("Working")
    #
    # # Testing case extraction
    # print("Visual inspection, check for duplicates:") #NOTE better test required
    # all = []
    # ex.extract_case("https://publications.parliament.uk/pa/ld199697/ldjudgmt/jd961121/smith01.htm", all)
    # for a in all:
    #     print(a)
    #
    # all = []
    # ex.extract_case("https://publications.parliament.uk/pa/ld200809/ldjudgmt/jd090617/attgen-1.htm", all)
    # for a in all:
    #     print(a)
    #
    # print("\n\nNEW CASE\n\n")
    #
    # all = []
    # ex.extract_case("https://publications.parliament.uk/pa/ld199697/ldjudgmt/jd961121/smith01.htm", all)
    # for a in all:
    #     print(a)
    #
    # print("\n\nNEW CASE\n\n")

    all = []
    ex.extract_case("https://publications.parliament.uk/pa/ld200506/ldjudgmt/jd060503/barker-1.htm", all)
    for a in all:
        print(a)
