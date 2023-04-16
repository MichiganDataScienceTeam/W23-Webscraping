import os, sys

import re
import matplotlib as plt
from matplotlib import pyplot
import pandas as pd
import numpy as np
import seaborn as sns
import bs4
import requests
import string

sys.path.append('/home/jason/MDST/webscraping/utils/')
from soup import getSoup


keywords = [
    'Join', 
    'joining', 
    'Here', 
    'Apply', 
    'Position', 
    'team', 
    'project', 
    'group', 
    'Opening', 
    'Available', 
    'Looking', 
    'Positions', 
    'recruiting'
    ]

def research_website(page):
    soup = getSoup(page)

    text = soup.get_text()
    words = text.split()


    words_found = []
    words_treated  = []
    table = str.maketrans(dict.fromkeys(string.punctuation)) 
    for word in words:
        words_treated.append(word.translate(table))
    for word in words_treated:
        for keyword in keywords:
            if word.casefold() == keyword.casefold():
                words_found.append(word)


    sentences = []
    punctuations = ['.','!','?']
    for index, word in enumerate(words):
        for keyword in keywords:
            if word.translate(table).casefold() == keyword.casefold():
                sentence = ''
                count = index
                while not words[count-1][-1] in punctuations:
                    count -= 1
                    sentence = words[count] + ' ' + sentence
                count = index
                while not words[count][-1] in punctuations:
                    sentence += words[count]
                    sentence += ' '
                    count += 1
                sentence += words[count]
                if len(sentence) < 1000:
                    sentences.append(sentence)


    links_all = soup.find_all('a')
    links = []
    for i in links_all:
        temp = i.text.strip()
        links.append(temp)

    keywords_links = ['Join', 'Here', 'Apply', 'Position', 'team', 'project', 'group', 'prospective']
    links_found = []
    for link in links:
        for keylink in keywords_links:
            if keylink.casefold() in link:
                if len(link) < 1000:
                    links_found.append(link)


    length_dif1 = len(words_found) - len(sentences)
    if length_dif1 > 0:
        while not length_dif1 == 0:
            sentences.append(" ")
            length_dif1 = len(words_found) - len(sentences)
    else:
        while not length_dif1 == 0:
            words_found.append(" ")
            length_dif1 = len(words_found) - len(sentences)


    length_dif2 = len(sentences) - len(links_found)
    if length_dif2 > 0:
        while not length_dif2 == 0:
            links_found.append(' ')
            length_dif2 = len(sentences) - len(links_found)
    else:
        while not length_dif2 == 0:
            sentences.append(' ')
            words_found.append(' ')
            length_dif2 = len(sentences) - len(links_found)

    tbl = dict()
    tbl['Keywords Found'] = words_found
    tbl['Sentences with keywords'] = sentences
    tbl['link names with keywords'] = links_found

    df = pd.DataFrame(data = tbl)

    points = {
                'Join' : 0, 
                'joining' : 1,
                'Here' : 0, 
                'Apply' : 0, 
                'Position' : 0, 
                'team' : 0, 
                'project' : 0, 
                'group' : 0, 
                'Opening' : 1, 
                'Available' : 0, 
                'Looking' : 0, 
                'Positions' : 0, 
                'recruiting' : 1,
                'apply here' : 1,
                'looking for' : 1
            }

    value = 0
    for sentence in sentences:
        for keyword in points:
            if keyword in sentence:
                if points[keyword] >  value:
                    value = points[keyword]

    return value    