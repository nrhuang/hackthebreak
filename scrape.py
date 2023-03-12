# import module
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

def get_job_url(url, job_title, location):

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
	
	driver.get(url)
   
	jobs_list = []
	jobs = driver.find_elements(By.CLASS_NAME, 'resultContent')
	jobs_count = len(jobs)
	for i in range(jobs_count):
		try:
			data = {
				"job_title":jobs[i].find_element(By.CLASS_NAME, 'jobTitle').text,
				"company_name":jobs[i].find_element(By.CLASS_NAME, 'companyName').text,
				"rating": 0
			}
		except IndexError:
			continue          
		jobs_list.append(data)
	
	return jobs_list

def get_review_url(company_name):
	return "https://ca.indeed.com/cmp/" + company_name + "/reviews?fcountry=CA&ftopic=jobsecadv"

def get_security_rating(url):
	
	driver.get(url)
	return driver.find_element(By.CLASS_NAME, 'css-1b9j5z0').text


def run():
	job_url = get_job_url('https://ca.indeed.com/','Data Scientist',"Vancouver")
	jobs = scrape_job_details(job_url)
	for job in jobs:
		rating_url = get_review_url(job["company_name"])
		job["rating"] = get_security_rating(rating_url)
	print(jobs)

run()
