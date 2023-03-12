# import module
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def get_current_url(url, job_title, location):

	driver = webdriver.Chrome()
	driver.get(url)
	time.sleep(1)
	driver.find_element(By.XPATH, '//*[@id="text-input-what"]').send_keys(job_title)
	time.sleep(1)
	driver.find_element(By.XPATH, '//*[@id="text-input-where"]').send_keys(Keys.CONTROL + "a")
	driver.find_element(By.XPATH, '//*[@id="text-input-where"]').send_keys(Keys.DELETE)
	time.sleep(1)
	driver.find_element(By.XPATH, '//*[@id="text-input-where"]').send_keys(location)
	time.sleep(1)
	driver.find_element(By.XPATH, "//form[@id='jobsearch']/button[1]").click()
	return driver.current_url

def scrape_job_details(url):
	
	driver = webdriver.Chrome()
	driver.get(url)
   
	jobs_list = []
	jobs = driver.find_elements(By.CLASS_NAME, 'resultContent')
	jobs_count = len(jobs)
	for i in range(jobs_count):
		try:
			data = {
				"job_title":jobs[i].find_element(By.CLASS_NAME, 'jobTitle').text,
				"company_name":jobs[i].find_element(By.CLASS_NAME, 'companyName').text
			}
		except IndexError:
			continue          
		jobs_list.append(data)
	print(jobs_list)
	dataframe = pd.DataFrame(jobs_list)
	
	return dataframe

current_url = get_current_url('https://ca.indeed.com/','Data Scientist',"Vancouver")
scrape_job_details(current_url)