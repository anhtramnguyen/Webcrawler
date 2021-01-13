# Webcrawler
Build Your Own Web Crawler

The goal of this project is to build a very simple web crawler which fetches URLs and outputs crawl results to stdout as the crawl proceeds.

Basic Crawler

The application takes as input a starting URL; it then performs the following:
1. Fetch the HTML document at that URL
2. Parse out URLs in that HTML document
3. Log/print the URL visited along with all the URLs on the page 
4. Loop back to step 1 for each of these new URLs

The application fetches multiple “levels” of pages, NOT just the first page and its immediate children.

Format of the output is as follows:

      URL of page fetched 
            URL found on page 
            URL found on page 
      URL of page fetched 
            URL found on page 
            URL found on page
      
  
  
Parallelizing

The application fetches URLs in parallel by using ThreadPoolExecutor from concurrent.futures


Test and Build

test.sh can be used to build and test the application.
Output are generated to stdout.
Output can be piped to an output file, such as below:

./test.sh > out 2>&1
