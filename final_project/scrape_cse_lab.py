import os, sys

import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


def scrape_lab(driver, files):
    profs = {}
    for lab, site in files:
        driver.get(site)
        read_page(driver, profs, lab)
        print(f'PROGRESS: {lab} completed')
    
    return list(profs.values())

def read_page(driver, profs, lab):  
    for faculty in driver.find_elements(by=By.XPATH, value='//div[@class="eecs_person_copy"]'):
        
        name = faculty.find_element(By.XPATH, './/h4').text
        if name in profs:
            profs[name]['lab'].append(lab)
            continue
        
        
        # standard info
        relevant_info = {
            'name': name,
            'title': faculty.find_element(By.XPATH, './/span[@class="person_title_section"]').text,
            'email': faculty.find_element(By.XPATH, './/a[@class="person_email"]').text,
            'lab': [lab]
        }
        
        # optional info - interests
        try: val = faculty.find_element(By.XPATH, './/span[@class="person_copy_section pcs_tall"]').text \
            [20:].strip('.').split(', ')
            if val[-1].startswith('and'): val[-1] = val[-1][3:].strip()
        except: val = None
            
        relevant_info['interests'] = val
        
        # optional info - website
        try: val = faculty.find_element(By.XPATH, './/a[@class="person_web"]').get_attribute('href')
        except Exception as e: val = None
        relevant_info['website'] = val
        
        # optional info - phone, office
        stubs = ['phone', 'office']
        for opt_field in faculty.find_elements(By.XPATH, './/span[@class="person_copy_section "]'):
            text = opt_field.text
            for x in stubs:
                if text.startswith(f'{x.title()}: '):
                    relevant_info[x] = text[len(x) + 2:]
        
        for x in stubs:
            if x not in relevant_info:
                relevant_info[x] = None
        # print(*relevant_info.items(), sep='\n')
        profs[name] = relevant_info
        
# files = [
#     'https://theory.engin.umich.edu/people/',
#     'https://ai.engin.umich.edu/people/',
#     'https://ce.engin.umich.edu/people/',
#     'https://hcc.engin.umich.edu/people/',
#     'https://systems.engin.umich.edu/people/',
#     'https://cse-teaching.engin.umich.edu/people/',
# ]
#      driver = 
#      li = scrape_lab(files)