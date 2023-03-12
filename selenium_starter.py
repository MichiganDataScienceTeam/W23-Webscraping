import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.add_experimental_option("detach", True) # this keeps the window open post execution/errors/ changing frames (explained later)

prefs = {"download.default_directory": '/Users/justinpaul/Downloads',  # note need to change this
         "directory_upgrade": True}
chrome_options.add_experimental_option("prefs", prefs)

# driver = webdriver.Chrome('/usr/local/bin/chromedriver')
driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=chrome_options)

driver.get('https://www.linkedin.com/')
WebDriverWait(driver, timeout=30)


driver.close()  # comment out if you want to keep it open