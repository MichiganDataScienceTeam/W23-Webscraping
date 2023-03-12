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
driver.get('https://www.mdst.club/agenda')

WebDriverWait(driver, timeout=5) # make sure DOM has loaded elements

# like before, it is easy to get some identifying information about the site
print(f'title of site: {driver.title}')

# you can also access and set cookies
print(f'initial cookies: {driver.get_cookies()}')
cookie = {'name' : 'MDSTcookie', 'value' : 'yum'}
driver.add_cookie(cookie)
print(f'cookies: {driver.get_cookies()}')

print('_'*30)

# you can also scroll!

time.sleep(2) # don't put in time.sleep() normally, use WebDriverWaits... I do just to show what it looks like
# driver.execute_script("window.scrollTo(0,document.body.scrollHeight-300)")


# As per usual, you can still search for elements by ID/class/...
for x in driver.find_elements(By.CLASS_NAME, 'C9DxTc '):
    print(x.text)
print('-'*30)

# The more standard/conventional way with selenium is with XPATH
for x in driver.find_elements(By.XPATH, '//span[@class="C9DxTc "]'):
    print(x.text)
print('_'*30)

# Some elements you can not interact with directly
try:
    driver.find_elements(By.XPATH, '//img[@id="navForward1"]')

except Exception as e:
    print(e) 
    print("There is a google calendar iframe embedded in the website, so to interact with it, we need to change our driver from the site to the iframe.")

# this is the normal way to deal with embedded elements/iframes when it gives you problems
calendar = driver.find_element(By.XPATH, "//iframe[@jsname='L5Fo6c']")

# to switch specifically you can use
driver.switch_to.frame(calendar)

time.sleep(2)
WebDriverWait(driver, timeout=2)
driver.find_element(By.XPATH, '//img[@id="navForward1"]').click()
time.sleep(2)

# driver.find_elements(By.XPATH, '//span[@class="te-s"]')[-1].click()  # this is equivalent
driver.find_elements(By.XPATH, '//*[@class="te-s"]')[-1].click()

time.sleep(2)
expo = driver.find_element(By.XPATH, '//div[@class="details"]')

# sample print out of card
print(expo.find_element(By.XPATH, '//span[@class="title"]').text)
print(expo.find_element(By.XPATH, '//span[@class="event-when"]').text)

links = expo.find_element(By.XPATH, '//span[@class="links"]')

for a_tag in links.find_elements(By.XPATH, '//a'):
    print(a_tag.text, a_tag.get_attribute('href'), sep='\t')

# Screenshotting!
driver.save_screenshot('selenium_full_screen.png')  # full screen
expo.screenshot('selenium_expo_card.png')  # individual element

driver.switch_to.default_content() # set driver back to site, not iframe
WebDriverWait(driver, timeout=5)

# time.sleep(10)  # can change this as well
driver.close()  # if you comment this out, the window will stay open even after it is done executing