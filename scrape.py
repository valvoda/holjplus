"""
Adapted from https://realpython.com/python-web-scraping-practical-introduction/
for the purpose of scraping https://publications.parliament.uk/pa/ld/ldjudgmt.HTML
to create an expanded HOLJ+ corpus

"""
import requests
from requests import get
from requests.exceptions import RequestException
from contextlib import closing

class Scrape:

    def simple_get(self, url):
        """
        Attempts to get the content at `url` by making an HTTP GET request.
        If the content-type of response is some kind of HTML/XML, return the
        text content, otherwise return None
        """
        try:
            with closing(get(url, stream=True)) as resp:
                if self.is_good_response(resp):
                    return resp.content
                else:
                    return None

        except RequestException as e:
            self.log_error('Error during requests to {0} : {1}'.format(url, str(e)))
            return None


    def is_good_response(self, resp):
        """
        Returns true if the response seems to be HTML, false otherwise
        """
        content_type = resp.headers['Content-Type'].lower()
        return (resp.status_code == 200
                and content_type is not None
                and content_type.find('html') > -1)


    def log_error(self, e):
        """
        It is always a good idea to log errors.
        This function just prints them, but you can
        make it do anything.
        """
        print(e)

if __name__ == "__main__":
    sc = Scrape()

    print("Testing the scaper:")
    raw_html = sc.simple_get('https://realpython.com/blog/')
    assert (len(raw_html) > 0), "Error, does not get"

    no_html = sc.simple_get("https://doesnotexist.com/thereshouldbenothing/")
    assert (no_html == None), "Error, does get"
    print("Working")
