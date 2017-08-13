
import requests
import re
from urllib.parse import urlparse

# In this example we're trying to collect e-mail addresses from a website

# Basic e-mail regexp:
# letter/number/dot/comma @ letter/number/dot/comma . letter/number
email_re = re.compile(r'([\w\.,]+@[\w\.,]+\.\w+)')

# HTML <a> regexp
# Matches href="" attribute
link_re = re.compile(r'href="(.*?)"')

def crawl(url, maxlevel):
    # Limit the recursion, we're not downloading the whole Internet
    if(maxlevel == 0):
        return

    # Get the webpage
    req = requests.get(url)
    result = []

    # Check if successful
    if(req.status_code != 200):
        return []

    # Find and follow all the links
    links = link_re.findall(req.text)
    for link in links:
        # Get an absolute URL for a link
        link = urlparse.urljoin(url, link)
        result += crawl(link, maxlevel - 1)

    # Find all emails on current page
    result += email_re.findall(req.text)
    return result

emails = crawl('http://localhost:8000', 2)

print("Scrapped e-mail addresses:")
for e in emails:
    print(e)
