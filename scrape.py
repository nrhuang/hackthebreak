# import module
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
from urllib.parse import parse_qs
import json

def get_job_url(url, job_title, location):

	driver = webdriver.Chrome()
	driver.get(url)
	driver.find_element(By.XPATH, '//*[@id="text-input-what"]').send_keys(job_title)
	driver.find_element(By.XPATH, '//*[@id="text-input-where"]').send_keys(Keys.CONTROL + "a")
	driver.find_element(By.XPATH, '//*[@id="text-input-where"]').send_keys(Keys.DELETE)
	driver.find_element(By.XPATH, '//*[@id="text-input-where"]').send_keys(location)
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
	
	driver = webdriver.Chrome()
	driver.get(url)
	return driver.find_element(By.CLASS_NAME, 'css-1b9j5z0').text


def run(url):

	parsed_url = urlparse(url)
	title = parse_qs(parsed_url.query)['title'][0]
	location = parse_qs(parsed_url.query)['location'][0]

	job_url = get_job_url('https://ca.indeed.com/',title,location)
	jobs = scrape_job_details(job_url)

	for job in jobs:
		rating_url = get_review_url(job["company_name"])
		try:
			job["rating"] = get_security_rating(rating_url)
		except:
			continue
	
	with open('jobs.json', 'w') as outfile:
		json.dump(jobs, outfile)
