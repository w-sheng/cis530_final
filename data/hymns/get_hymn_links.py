from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 
           'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'y', 'z']

with open('hymn_links.txt', 'w') as f:
    for letter in letters:
        url = 'https://www.hymnlyrics.org/newlyrics_all/' + letter + '.php'

        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        page = urlopen(req).read()
        soup = BeautifulSoup(page, 'html.parser')

        tags = soup.find_all('p', 'MsoNormal')

        for tag in tags:
            a = tag.a
            if a and a['href']:
                f.write((tag.a)['href'] + '\n')
        