import requests
from bs4 import BeautifulSoup
from queue import Queue, Empty
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse
import functools
import sys
import getopt

NUM_WORKERS = 10 #30

class basicCrawlerWithPool:

    def __init__(self, url):

        self._url = url
        self.prefix_url = '{}://{}'.format(urlparse(self._url).scheme, urlparse(self._url).netloc)

        self.fetched_pages = set([])
        self.found_pages = Queue()
        self.found_pages.put(self._url)
        self.executor = ThreadPoolExecutor(max_workers=NUM_WORKERS)


    def request_page(self, url):
        try:
            page = requests.get(url, timeout=(3, 27))
            return page
        except requests.RequestException:
            return

    def printlist(self, items):
        for item in items:
            print( "    ", item)

    # parse the page content of url for href.
    # all found urls are printed to stdout, but only those urls that starts with prefix_url (see init function)
    # are added to queue found_pages, to be fetched.
    #
    def parse_page(self, htmlpage, url):
        bsoup = BeautifulSoup(htmlpage, 'html.parser')
        hrefs = bsoup.find_all('a', href=True)

        print(url)
        local_pages = set([])

        for ref in hrefs:
            nestedUrl = ref['href']

            if nestedUrl.startswith('/') or nestedUrl.startswith(self.prefix_url):
                nestedUrl = urljoin(self.prefix_url, nestedUrl)

                if nestedUrl not in self.fetched_pages:
                    if nestedUrl not in local_pages:   # this is not to add duplicates to found_pages queue
                        self.found_pages.put(nestedUrl)
                local_pages.add(nestedUrl)

            elif nestedUrl.startswith("http"):
                local_pages.add(nestedUrl)

        self.printlist(local_pages)

    # callback for ThreadPoolExecutor
    def callback(self, url, response):
        result = response.result()
        if result and result.status_code == 200:
            self.parse_page(result.text, url)


    def run(self):
        while True:
            try:
                pageurl = self.found_pages.get(timeout=60)
                if pageurl not in self.fetched_pages:
                    self.fetched_pages.add(pageurl)
                    task = self.executor.submit(self.request_page, pageurl)
                    #use functools as wrapper to add extra parameter to callback function
                    task.add_done_callback(functools.partial(self.callback, pageurl))
            except Empty:
                return
            except Exception as err:
                print(err)
                continue


def main(argv):
    # Get full command-line arguments
    full_cmd_arguments = sys.argv

    argument_list = full_cmd_arguments[1:]
    short_options = "hu:m:"
    long_options = ["help", "url", "max"]

    url = ''
    try:
        arguments, values = getopt.getopt(argument_list, short_options, long_options)
    except getopt.error as err:
        # Output error, and return with an error code
        print (str(err))
        sys.exit(2)

    for opt, arg in arguments:
         if opt == '-h':
             print ('basicwebcrawler.py -u <url>')
             print ('e.g. basicwebcrawler.py -u https://www.example.com')
             sys.exit()
         elif opt in ("-u", "--url"):
             url = arg

    crawler = basicCrawlerWithPool(url)
    crawler.run()

if __name__ == "__main__":
   main(sys.argv[1:])
