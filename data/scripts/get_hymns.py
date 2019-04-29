'''
Given a list of hymn urls from https://www.hymnlyrics.org/content/search_letter.php, 
use the beautiful soup library to aggregate all the actual hymn lyrics into one file.
'''

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

hymn_links_file = 'hymn_links.txt'
hymns_file = 'hymns.txt'

with open(hymns_file, 'w') as file:
    for url in open(hymn_links_file, 'r'):
        try:
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            page = urlopen(req).read()
            soup = BeautifulSoup(page, 'html.parser')

            spans = soup.find_all('span', eza=True)

            for span in spans:
                poem = span.text
                if poem and len(poem) > 3:
                    file.write(url)
                    # file.write(''.join(map(lambda x : str(x), poem)))
                    file.write(poem + '\n')
                    print(url)
                    break
        except:
            continue 


        