from bs4 import BeautifulSoup
import requests


def getSoup(url: str) -> BeautifulSoup:
    page = requests.get(url)
    bs = BeautifulSoup(page.content, "html.parser")
    page.close()
    
    return bs
