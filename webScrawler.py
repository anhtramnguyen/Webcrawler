# Basic Crawler
# The goal of this project is to build a very simple web crawler which fetches URLs
# and outputs crawl results to some sort of log or console as the crawl proceeds.
#
# Format of the output as follows:
# <URL of page fetched> <URL found on page> <URL found on page> ....
# <URL of page fetched> <URL found on page> <URL found on page>
#
# Output is to stdout.

import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
import re
import sys
import getopt

global_list = []  #list of urls

# add the link as-is or generate a new url and add to local_list
def get_full_url(url, link, local_list):
    if len(link) > 1 and link.startswith("/"):
        if (url.endswith("/")):
            url = url[:-1]   #remove the trailing / in url
        newlink = url+link   #append sublink to url
        if (newlink not in local_list):
            local_list.append(newlink)  #add new url to local_list
    elif link.startswith("http") and link not in local_list:
        local_list.append(link)         #add url to local_list

# print all items in global_list
def print_global_list():
    # print("global_list: ****")
    for url in global_list:
        print(url)

# print all items in local_list, each prefixed with a tab
def print_list( list ):
    for url in list:
        print("     ", url)

#add items in local_list to global_list
def extend_list(global_list, local_list):
    for item in local_list:
        if item not in global_list:
            global_list.append(item)


def parse_a_url(url):
    if (url != None):
        local_list = []
        try:
            pageS = requests.get(url)
            soupS = BeautifulSoup(pageS.content, "html.parser")

            # Pull text from all instances of <a> tag
            a_items = soupS.find_all('a')

            for name in a_items:
                link = name.get('href')
                if (link != None):
                    get_full_url(url, link, local_list)

            #print
            print(url)
            print_list(local_list)
            extend_list(global_list, local_list) # add to global_list
        except requests.exceptions.ConnectionError:
            print("Connection refused by the server for ", url)


def crawl_with_pool(url):
    parse_a_url(url)

    with Pool(10) as p:
        p.map(parse_a_url, global_list)

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
             print ('webScrawler.py -u <url>')
             print ('e.g. webScrawler.py -u https://www.rescale.com')
             sys.exit()
         elif opt in ("-u", "--url"):
             url = arg

    global_list = []
    crawl_with_pool(url)

if __name__ == "__main__":
   main(sys.argv[1:])
