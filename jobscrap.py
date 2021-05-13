from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

import pandas as pd
import requests
import time
import json
import math
import sys

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome('chromedriver', options=options)
time.sleep(2)
base_url = "https://www.jobstreet.co.id/en/job-search/{}-jobs/{}/"

def get_page_number(keyword):
    #input: keyword for job_postings
    #output: number of pages

    url = base_url.format(keyword, 1)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    result_text = soup.find("span",{"class": "FYwKg _2Bz3E C6ZIU_0 _1_nER_0 _2DNlq_0 _29m7__0 _1PM5y_0"})
    results = result_text.text.split()
    result = int(result_text.text.replace(',', '').split()[-2])
    print(results, result)
    page_number = math.ceil(result/30)
    
    return page_number

def job_page_scraper(link):
    url = "https://www.jobstreet.co.id"+link
    print("scraping...", url)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    scripts = soup.find_all("script")

    for script in scripts:
        if script.contents:
            txt = script.contents[0].strip()
            if 'window.REDUX_STATE = ' in txt:
                jsonStr = script.contents[0].strip()
                jsonStr = jsonStr.split('window.REDUX_STATE = ')[1].strip()
                jsonStr = jsonStr.split('}}}};')[0].strip()
                jsonStr = jsonStr+"}}}}"
                jsonObj = json.loads(jsonStr)
    
    try:
        job = jsonObj['details']
        job_id = job['id']
        job_title = job['header']['jobTitle']
        company = job['header']['company']['name']
        job_post_date = job['header']['postedDate']
        job_requirement_career_level = job['jobDetail']['jobRequirement']['careerLevel']
        company_size = job['companyDetail']['companySnapshot']['size']
        company_industry = job['jobDetail']['jobRequirement']['industryValue']['label']
        job_description = job['jobDetail']['jobDescription']['html']
        job_employment_type = job['jobDetail']['jobRequirement']['employmentType']
        job_function = ', '.join([x['name'] for x in job['jobDetail']['jobRequirement']['jobFunctionValue']])
        return [job_id, job_title, company, job_post_date, job_requirement_career_level, company_size, company_industry, job_description, job_employment_type, job_function]
    except Exception as e:
        print(e)
        return

def page_crawler(keyword):
    # input: keyword for job postings
    # output: dataframe of links scraped from each page

    # get total page number
    # page_number = get_page_number(keyword)
    page_number = 2
    job_links = []

    for n in range(page_number):
        print('Loading page {} ...'.format(n+1))
        url = base_url.format(keyword, n+1)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
    
        #extract all job links
        links = soup.find_all('a',{'class':'DvvsL_0 _1p9OP'})
        job_links += links
 
    jobs = []

    for link in job_links:
        job_link = link['href'].strip().split('?', 1)[0]
        job_desc = job_page_scraper(job_link)
        if job_desc is not None:
            job_desc = ['None' if v is None else v for v in job_desc]
            jobs.append([job_link] + job_desc)

    result_df = pd.DataFrame(jobs, columns = ['link', 'job_id', 'job_title', 'company', 'job_post_date', 'job_requirement_career_level', 'company_size', 'company_industry', 'job_description', 'job_employment_type', 'job_function'])
    return result_df

if __name__ == '__main__':
    # a list of job roles to be crawled
    key_words = ['data engineer', 'data analyst']
    # check if the time is between 00.00 and 01.00
    if time.gmtime().tm_hour >= 1:
        sys.exit()

    for key in key_words:
        key_df = page_crawler(key)
        data_dict = key_df.to_dict("records")
        url = "https://jobstreetscrap-api.herokuapp.com/jobs/?apiKey=1234567asdfgh"
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        resp = requests.post(url, data=json.dumps(data_dict), headers=headers)
        print(resp.json())
        
    driver.quit()
