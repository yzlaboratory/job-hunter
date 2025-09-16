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

def handleJobPosting(title, link):
    if(len(ac.findall(title)) != 0):
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
    if(len(recentpostings['jobs']) != 0):
        oldpostings['jobs'].extend(recentpostings['jobs'])
else:
    oldpostings = recentpostings

keywords = []
with open("data/dictionary") as file:
    keywords = [line.rstrip() for line in file]
builder = AcoraBuilder(keywords)
ac = builder.build()

companies = dict()
with open('data/inputs.json') as json_file:
    companies = json.load(json_file)

newpostings = { "jobs" : []}

#use selenium headless to search inputurls 
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless=new")
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
                handleJobPosting(title.get_property('title'),job.get_attribute('href'))
        except NoSuchElementException:
            print("No current postings jor Jobrad")
driver.quit()
with open('data/newjobs.json', 'w') as json_file:
    json.dump(newpostings, json_file, default=str)
with open('data/oldjobs.json', 'w') as json_file:
    json.dump(oldpostings, json_file, default=str)
#WRITE POSTINGS IN FILE json format
#WRITE OLD POSTINGS IN FILE old postings

# write wrappers for every single inputurls because gthese sites differ
# wanted output is job postings in data structure with url, jobname, posted date and locations
