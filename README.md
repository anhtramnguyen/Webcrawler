# Webcrawler
Build Your Own Web Crawler

The goal of this project is to build a very simple web crawler which fetches URLs and outputs crawl results to some sort of log or console as the crawl proceeds.

Basic Crawler

The application takes as input a starting URL; it then performs the following:
1. Fetch the HTML document at that URL
2. Parse out URLs in that HTML document
3. Log/print the URL visited along with all the URLs on the page 
4. Loop back to step 1 for each of these new URLs

The application fetches multiple “levels” of pages, NOT just the first page and its immediate children.

Format of the output as follows:

      URL of page fetched 
            URL found on page 
            URL found on page 
      URL of page fetched 
            URL found on page 
            URL found on page
      
  
  
Parallelizing

The application fetch URLs in parallel by using Multiprocessing


Test and Build

test.sh can be used to build and test the application.
Output will be generated to stdout.
I would suggest to pipe test.sh to an output file, such as below:

./test.sh > out 2>&1
