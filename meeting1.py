import re

from utils.soup import getSoup
from utils.caesar_cipher_enc_dec import decode

# page = f'http://127.0.0.1:5000/caesar/'
page = 'https://www.mdst.club/projects'
soup = getSoup(page)

soup.find_all('p')