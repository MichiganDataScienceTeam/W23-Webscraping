import re

from utils.soup import getSoup
from utils.caesar_cipher_enc_dec import decode

def unscramble_art(art='dogs'):
    page = f'http://127.0.0.1:5000/shuffled_art/{art}/'

    soup = getSoup(page)

    inst = soup.find_all(class_=re.compile('row_\d+'))
    
    li = [(x.text.strip().replace('H', ' '), int(x.get('class')[0].split('_')[-1])) for x in inst]

    sorted_li = [x[0] for x in sorted(li, key= lambda x: x[1])]

    for x in sorted_li:
        print(x)
        


def uncaesar():
    page = 'http://127.0.0.1:5000/caesar/'
    
    soup = getSoup(page)
    ciphers = soup.find_all(id=re.compile('row_\d+'))
    
    for c in ciphers:
        t = c.text.strip()
        k = c.get('id').split('_')[-1].strip()
        
        print(decode(t, k))


def scrape_mdst():
    page = 'https://www.mdst.club/projects'
    
    soup = getSoup(page)
    
    dir_tags = [x for x in soup.find_all('p', dir = 'ltr')]
    
    dir_tags = soup.find_all('p', class_='zfr3Q')
    
    soup.find_all('p', class_='CDt4Ke')
    x = dir_tags[0]
    print(x)
    
    print(*[x.text for x in soup.find_all(dir = 'ltr')], sep='\n')

