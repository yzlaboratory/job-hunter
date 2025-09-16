import json
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from acora import AcoraBuilder
from selenium.common.exceptions import TimeoutException

keywords = []
with open("data/dictionary") as file:
    keywords = [line.rstrip() for line in file]
print(keywords)
builder = AcoraBuilder(keywords)
ac = builder.build()
companies = dict()
with open('data/inputs.json') as json_file:
    companies = json.load(json_file)
    print(companies['companies'][0])


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
            print(len(postings))
            for job in postings:
                title = job.find_element(By.CLASS_NAME, 'title')
                if(len(ac.findall(title.get_property('title'))) != 0):
                   print(title.get_property('title'))
                   print(job.get_attribute('href'))
        except NoSuchElementException:
            print("No current postings jor Jobrad")
driver.quit()
# write wrappers for every single inputurls because gthese sites differ
# wanted output is job postings in data structure with url, jobname, posted date and locations