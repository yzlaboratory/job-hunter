import json
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from acora import AcoraBuilder
from selenium.common.exceptions import TimeoutException
import datetime
import os

def handleJobPosting(title, link, company):
    print("Found 1 recent job posting at " + company)
    if(len(ac.findall(title)) != 0):
        #printl
        posting = {
            "title" : title,
            "link" : link,
            "date" : datetime.date.today()
        }
        if(not oldpostings or not any(x['link']==posting['link'] for x in oldpostings['jobs'])):     
            newpostings['jobs'].append(posting)
    
recentpostings = dict()
if(os.stat("data/newjobs.json").st_size != 0):
    with open('data/newjobs.json') as json_file:
        recentpostings = json.load(json_file)

oldpostings = dict()
if(os.stat("data/oldjobs.json").st_size != 0):
    with open('data/oldjobs.json') as json_file:
        oldpostings = json.load(json_file)

if(oldpostings):
    if(recentpostings and len(recentpostings['jobs']) != 0):
        oldpostings['jobs'].extend(recentpostings['jobs'])
else:
    oldpostings = recentpostings

keywords = []
with open("data/dictionary") as file:
    keywords = [line.rstrip() for line in file]
builder = AcoraBuilder(keywords)
ac = builder.build()
print(keywords)

companies = dict()
with open('data/inputs.json') as json_file:
    companies = json.load(json_file)

newpostings = { "jobs" : []}

#use selenium headless to search inputurls 
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--headless=new")
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(5)

for i in companies['companies']:
    if(i['Name']=='Jobrad'):
        driver.get(i['Url'])
        delay = 10
        try: WebDriverWait(driver, delay).until(EC.staleness_of(driver.find_element(By.CLASS_NAME, 'loading-result-item')))
        except TimeoutException:
            print("Internet too slow")
        try:
            postings = driver.find_elements(By.CSS_SELECTOR, 'a.result-item')
            for job in postings:
                title = job.find_element(By.CLASS_NAME, 'title')
                handleJobPosting(title.get_property('title'),job.get_attribute('href'),"Jobrad")
        except NoSuchElementException:
            print("No current postings for Jobrad")
    if(i['Name']=='Google'):
        driver.get(i['Url'])
        try:
            postings = driver.find_elements(By.CLASS_NAME, 'lLd3Je')
            for job in postings:
                title = job.find_element(By.CLASS_NAME, 'QJPWVe').text
                href = job.find_element(By.TAG_NAME, 'a').get_attribute('href')
                handleJobPosting(title,href,"Google")
        except NoSuchElementException:
            print("No current postings for Google")
    if(i['Name']=='Meta'):
        driver.get(i['Url'])
        try:
            postings = driver.find_elements(By.CSS_SELECTOR, 'a.x1ypdohk.x1lku1pv')
            for job in postings:
                title = job.find_element(By.CSS_SELECTOR, 'div._6g3g.x10lme4x.x26uert.xngnso2.x117nqv4.x1mnlqng.x1e096f4').get_attribute('textContent')
                href = job.get_attribute('href')
                handleJobPosting(title,href,"Meta")
        except NoSuchElementException:
            print("No current postings for Meta")
    if(i['Name']=='Apple'):
        driver.get(i['Url'])
        try:
            postings = driver.find_elements(By.XPATH, "//*[contains(@class, 'job-list-item')]/div[1]/h3/a")
            for job in postings:
                title = job.get_attribute('textContent')
                href = job.get_attribute('href')
                handleJobPosting(title,href,"Apple")
        except NoSuchElementException:
            print("No current postings for Apple")
    if(i['Name']=='Snap'):
        driver.get(i['Url'])
        try:
            postings = driver.find_elements(By.XPATH, '//article/div/div/table/tbody/tr')
            for job in postings:
                cell = job.find_element(By.XPATH,'//td[1]')
                link = cell.find_element(By.TAG_NAME, 'a')
                title = link.find_element(By.TAG_NAME, 'span').get_attribute('textContent')
                href = link.get_attribute('href')
                handleJobPosting(title,href,"Snap")
        except NoSuchElementException:
            print("No current postings for Snap")
    if(i['Name']=='Nvidia'):
        driver.get(i['Url'])
        try:
            postings = driver.find_elements(By.XPATH, '//*[@id="mainContent"]/div/div[2]/section/ul/li')
            for job in postings:
                try:
                    link = job.find_element(By.TAG_NAME, 'a')
                    title = link.get_attribute('textContent')
                    href = link.get_attribute('href')
                except NoSuchElementException:
                    print("1 Broken Entry at Nvidia")
                handleJobPosting(title,href,"Nvidia")
        except NoSuchElementException:
            print("No current postings for Nvidia")
    if(i['Name']=='Dfinity'):
        driver.get(i['Url'])
        try:
            postings = driver.find_elements(By.XPATH, '//div[@class="job-posts--table"]/table/tbody/tr')
            for job in postings:
                link = job.find_element(By.TAG_NAME, 'a')
                title = link.find_element(By.CSS_SELECTOR,'p.body--medium').get_attribute('textContent')
                href = link.get_attribute('href')
                handleJobPosting(title,href,"Dfinity")
        except NoSuchElementException:
            print("No current postings for Dfinity")
    if(i['Name']=='IBM'):
        driver.get(i['Url'])
        try:
            postings = driver.find_elements(By.XPATH, '//*[@id="ibm-hits-wrapper"]/div/div')
            for job in postings:
                title = job.get_attribute("aria-label")
                href = job.find_element(By.TAG_NAME, 'a').get_attribute('href')
                handleJobPosting(title,href,"IBM")
        except NoSuchElementException:
            print("No current postings for IBM")
    if(i['Name']=='Epic Games'):
        driver.get(i['Url'])
        try:
            postings = driver.find_elements(By.XPATH, '//*[@id="epicGamesReactWrapper"]/div/div/div/div/div/div/div[3]/div[4]/a')
            for job in postings:
                title = job.find_element(By.CLASS_NAME, 'joblisting-title').find_element(By.TAG_NAME, 'span').get_attribute("textContent")
                href = job.get_attribute('href')
                handleJobPosting(title,href,"Epic Games")
        except NoSuchElementException:
            print("No current postings for Epic Games")
    if(i['Name']=='GetYourGuide'):
        driver.get(i['Url'])
        delay = 10
        try: WebDriverWait(driver, delay).until(EC.element_to_be_clickable(driver.find_element(By.ID, 'reset-filter')))
        except TimeoutException:
            print("Internet too slow")
        try:
            postings = driver.find_elements(By.CSS_SELECTOR, 'a.open-roles-item')
            for job in postings:
                title = job.find_element(By.TAG_NAME, 'h5').get_attribute("textContent")
                href = job.get_attribute('href')
                handleJobPosting(title,href,"GetYourGuide")
        except NoSuchElementException:
            print("No current postings for GetYourGuide")
driver.quit()
with open('data/newjobs.json', 'w') as json_file:
    json.dump(newpostings, json_file, default=str)
with open('data/oldjobs.json', 'w') as json_file:
    json.dump(oldpostings, json_file, default=str)