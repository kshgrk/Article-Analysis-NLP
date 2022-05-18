from bs4 import BeautifulSoup
import pandas as pd
from urllib.request import Request
from urllib.request import urlopen

inp = pd.read_excel('Input.xlsx')

def getData(url):
    raw_request = Request(url)
    raw_request.add_header('User-Agent', 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11')
    raw_request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
    resp = urlopen(raw_request)
    raw_html = resp.read()
    soup = BeautifulSoup(raw_html, 'html.parser')
    title = soup.find('h1').text
    container = soup.find('div', attrs={'class':'td-post-content'})
    body = ' '.join([x.text for x in container.find_all('p') if x.text != " "])
    body = body.replace('\n', ' ').replace('\r', ' ')
    return title, body

for i in range (1, inp.shape[0]+1):
    title, body = getData(inp['URL'].iloc[i-1])
    fname = 'Scraped Data/'+str(i)+'.txt'
    f = open(fname, 'w')
    l = [title,"\n", body]
    f.writelines(l)
    f.close()