from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv, time, os, json

class Freelancermap_Scrapper():
    def __init__(self):
        self.input_file = 'Credentials.json'
        self.output_file = 'Freelancermap_Data.csv'
    
    def read_json(self):
        with open(self.input_file,'r') as f:
            read_credentials = json.load(fp=f)
        email = read_credentials.get('email','')
        password = read_credentials.get('password','')
        return email, password
    
    def login_process(self,driver,email,password):
        accpect_cookies = driver.find_element(By.XPATH,'//button[@id="onetrust-accept-btn-handler"]')
        accpect_cookies.click()
        time.sleep(1)
        login_btn = driver.find_element(By.XPATH,'//a[@id="login-btn"]')
        login_btn.click()
        time.sleep(2)
        email_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//input[@id="login"]')))
        email_input.send_keys(email)
        time.sleep(1)
        password_input = driver.find_element(By.XPATH,'//input[@id="password"]')
        password_input.send_keys(password)
        time.sleep(2)
        password_input.send_keys(Keys.ENTER)
        time.sleep(3)
        print(f'[INFO] Login Successful!')
    
    def get_all_urls(self,driver):
        urls_tags = driver.find_elements(By.XPATH,'//a[@class="project-title"]')
        all_urls = [tag.get_attribute('href') for tag in urls_tags]
        return all_urls    
    
    def extract_data(self,driver,all_urls):
        for url in all_urls:
            driver.get(url)
            time.sleep(3)
            title = driver.find_element(By.XPATH,'//div[@id="project"]//h1').text
            description = driver.find_element(By.XPATH,'//div[@class="content"]').get_attribute('textContent').replace('Beschreibung','').strip()
            date = driver.find_element(By.XPATH,'//div[@itemprop="datePosted"]').text
            row = [title,date,description]
            print(f'[INFO] Getting Job: {title}')
            self.save_data(row)
    
    def save_data(self,row):
        with open(self.output_file,'a',newline='',encoding='utf-8') as f:
            csv.writer(f).writerow(row)
    
    def csv_header(self):
        header = ['Title','Date','Description']
        with open(self.output_file,'w',newline='',encoding='utf-8') as f:
            csv.writer(f).writerow(header)
    
    def run(self):
        if self.input_file in os.listdir():
            if self.output_file not in os.listdir(): self.csv_header()
            email, password = self.read_json()
            driver = webdriver.Chrome()
            web_url = 'https://www.freelancermap.de/'
            driver.get(web_url)
            time.sleep(3)
            print(f'[INFO] Login website!')
            self.login_process(driver,email,password)
            url = 'https://www.freelancermap.de/projektboerse.html?projectContractTypes%5B0%5D=contracting&remoteInPercent%5B0%5D=100&industry%5B0%5D=24&countries%5B%5D=1&sort=1&pagenr='
            page = 1
            while True:
                main_url = f'{url}{page}'
                print(f'[INFO] Getting main Url:- {main_url}')
                driver.get(main_url)
                time.sleep(3)
                all_urls = self.get_all_urls(driver)
                if all_urls != [] and len(all_urls) > 1:
                    self.extract_data(driver,all_urls)
                    page += 1
                else:
                    break
        else:
            print(f'[INFO] No Credentials file ({self.input_file}) in directory...')

if __name__ == '__main__':
    scrapper = Freelancermap_Scrapper()
    scrapper.run()
            
            
            
            
        
    