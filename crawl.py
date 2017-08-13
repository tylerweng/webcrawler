from html.parser import HTMLParser
from urllib.parse import urljoin
import requests
import argparse
import re

# Basic e-mail regexp:
# letter/number/dot/comma @ letter/number/dot/comma . letter/number
email_re = re.compile(r'([\w\.,]+@[\w\.,]+\.\w+)')

# HTML <a> regexp
# Matches href="" attribute
link_re = re.compile(r'href="(.*?)"')

# class LinkParser(HTMLParser):
#     def __init__(self):
#         self.links = None
#         self.base_url = None
#
#     # This is a function that HTMLParser normally has
#     # but we are adding some functionality to it
#     def handle_starttag(self, tag, attrs):
#         if tag == 'a':
#             for (key, value) in attrs:
#                 if key == 'href':
#                     new_url = urljoin(self.base_url, value)
#                     self.links.append(new_url)
#
#     def get_links(self, url):
#         print("get_links()")
#         self.links = []
#         self.base_url = url
#         res = requests.get(url)
#         print("response", res)
#         obj = res.json()
#         # print("obj", obj)
#         print("type(obj)", type(obj))
#         print("obj[0]", obj[0])
#         # if True:
#         #
#         #     self.feed(html_string)
#         #     return html_string, self.links
#         # else:
#         #     return "", []


def crawl(url, maxlevel):
    print("maxlevel", maxlevel)
    print('url', url)
    # Limit the recursion, we're not downloading the whole Internet
    if(maxlevel == 0):
        return []

    # Get the webpage
    req = requests.get(url)
    result = []
    print("result", result)

    # Check if successful
    if(req.status_code != 200):
        return []

    # Find and follow all the links
    links = link_re.findall(req.text)
    print("links", links)
    for link in links:
        # Get an absolute URL for a link
        link = urljoin(url, link)
        result += crawl(link, maxlevel - 1)

    # Find all emails on current page
    emails = email_re.findall(req.text)
    for e in emails:
        if e not in result:
            result.append(e)

    return result

def spider(url, term, limit):
    pages_to_visit = [url]
    number_visited = 0
    found_term = False
    # The main loop. Create a LinkParser and get all the links on the page.
    # Also search the page for the term or string
    # In our getLinks function we return the web page
    # (this is useful for searching for the term)
    # and we return a set of links from that web page
    # (this is useful for where to go next)
    while number_visited < limit and pages_to_visit != [] and not found_term:
        number_visited = number_visited + 1
        # Start from the beginning of our collection of pages to visit:
        url = pages_to_visit[0]
        pages_to_visit = pages_to_visit[1:]
        try:
            print(number_visited, "Visiting:", url)
            parser = LinkParser()
            print("parser", parser)
            data, links = parser.get_links(url)
            print("data", data)
            if data.find(term) > -1:
                found_term = True
                # Add the pages that we visited to the end of our collection
                # of pages to visit:
                pages_to_visit = pages_to_visit + links
                print(" **Success!**")
        except:
            print(" **Failed!**")
    if found_term:
        print("Term: {term} found at url: {url}".format(term=term, url=url))
    else:
        print("Term: {term} never found".format(term=term))


def parse_args():
    parser = argparse.ArgumentParser(prog='crawl.py', description='Crawl links')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('--url', action='store', help='initial url to crawl')
    # parser.add_argument('--term', action='store', help='search term')
    parser.add_argument('--limit', action='store', type=int, help='number of pages to store')
    return parser.parse_args().__dict__


def main():
    args = parse_args()
    url = args["url"]
    # term = args["term"]
    limit = args["limit"]
    # spider(url, term, limit)
    emails = crawl(url, limit)
    print("Scrapped e-mail addresses:")
    for e in emails:
        print(e)

main()
