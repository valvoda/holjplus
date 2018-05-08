# HOLJ Plus

This project extracts UK House of Lords judgements from 1996 to 2009: https://publications.parliament.uk/pa/ld/ldjudgmt.htm

HTML files are scraped for the text of the cases and cleaned up for the purposes of annotating the majority judgement.
We select 231 of those cases and merge them with the [HOLJ corpus](https://www.inf.ed.ac.uk/research/isdd/admin/package?download=84) to create the 300 cases strong [HOLJ+ corpus](https://github.com/valvoda/holjplus/blob/master/HOLJ%2B.zip).

## Getting Started

To get the full corpus used in our research, simply run holjplus.py

### Prerequisites

* [NLTK](https://www.nltk.org/install.html)
* [BeautifulSoup 4](https://pypi.org/project/beautifulsoup4/)

## Running the tests

To run the build in tests, run format.py, extract.py and scrape.py

## Contributing

[scrape.py](https://realpython.com/python-web-scraping-practical-introduction/) - functions adapted from realpython.com tutorial

## Authors

* **Josef Valvoda**

## License

This project is licensed under the MIT License - [LICENSE.md](LICENSE)
