from bs4 import BeautifulSoup
import requests


def getSoup(url):
    page = requests.get(url)
    return BeautifulSoup(page.content, "html.parser")
