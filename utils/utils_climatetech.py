import os 

import boto3
from loguru import logger
from dotenv import load_dotenv
from selenium.webdriver import Remote
from selenium.webdriver.common.by import By
from botocore.exceptions import ClientError

from utils.utils_global import wait_for_element_to_load, findelement, findelement_getattribute
from utils.utils_decorator import handle_general_exceptions, handle_find_element_exceptions

load_dotenv()

class ClimateTech:
    def __init__(self, driver: Remote, website_link: str):
        self.driver = driver
        self.website_link = website_link
        self.job_title = None
        self.company_name = None
        self.job_description = None
        self.job_url = None
        self.job_location = None
        self.salary = None
        self.commitment = None
        self.company_website = None
        self.company_logo = None
        self.company_description = None
        self.company_location = None
        self.total_equity_funding = None
        self.vertical = None
        self.size = None
        self.stage = None
        self.last_funding_date = None
        self.investors = None
        self.company_href = None
        self.data = None
        self.linkedin_page = None
        self.links = []
        self.id = None
        self.dynamodb = boto3.resource(
            'dynamodb',
            region_name = 'eu-north-1',
            aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY'),
            )

        
    @handle_general_exceptions
    async def run_scraper(self):
        self.driver.get(self.website_link)
        if self.access_denied():
            return None
        self.get_job_links()
        for id,link in enumerate(self.links):
            if isinstance(link, str):
                self.id = id
                self.driver.get(link)
                self.job_url = link
                self.position()
                self.job_location = findelement(self.driver, By.XPATH, "//td[text()='Location']/following-sibling::td","job_location")
                self.salary = findelement(self.driver, By.XPATH, "//td[text()='Salary']/following-sibling::td","salary")
                self.commitment = findelement(self.driver, By.XPATH, "//td[text()='Commitment']/following-sibling::td","commitment")
                self.job_description = findelement(self.driver, By.XPATH,"//h1[text()='Job Description']/following-sibling::* | //h2[text()='Job Description']/following-sibling::*","job_description")
                self.company_href = findelement_getattribute(self.driver, By.XPATH, "//a[contains(., 'Company Info →')]", "href", "company_href")
                if isinstance(self.company_href, str):
                    self.driver.get(self.company_href)
                    self.com_vertical()
                    self.subvertical = findelement(self.driver, By.XPATH, "//td[text()='Subvertical']/following-sibling::td","subvertical")
                    self.size = findelement(self.driver, By.XPATH, "//td[text()='Size']/following-sibling::td","size")
                    self.stage = findelement(self.driver, By.XPATH, "//td[text()='Stage']/following-sibling::td","stage")    
                    self.linkedin_page = findelement(self.driver, By.XPATH, "//td[text()='LinkedIn page']/following-sibling::td","linkedin_page")    
                    self.total_equity_funding = findelement(self.driver, By.XPATH, "//td[text()='Total equity funding	']/following-sibling::td","total_equity_funding")  
                    self.last_funding_date = findelement(self.driver, By.XPATH, "//td[text()='Last Funding Date']/following-sibling::td","last_funding_date")
                    self.investors = findelement(self.driver, By.XPATH,"//td[text()='Investors']/following-sibling::td","investors")
                    self.company_location = findelement(self.driver, By.XPATH,"//td[text()='Location']/following-sibling::td", "company_location")
                    self.company_website = findelement(self.driver, By.XPATH,"//td[text()='Website']/following-sibling::td", "company_website")
                    self.company_logo = findelement_getattribute(self.driver, By.CSS_SELECTOR, "div.css-1jgxixz img", "src", "company_logo")
                    self.company_description = findelement(self.driver, By.XPATH,"//h1[contains(., 'Company Info')]/following-sibling::* | //h2[contains(., 'Company Info')]/following-sibling::* | //h3[contains(., 'Company Info')]/following-sibling::*","company_description")
                    self.get_scrapper()                
                    self.insert_into_dynamodb(self.data)
        return {"status":"Done"}
    
    
    @handle_find_element_exceptions
    def access_denied(self):
        message_xpath = "//h1[contains(text(), 'Access Denied')] | //h2[contains(text(), 'Access Denied')]"
        self.driver.find_element(By.XPATH, message_xpath)
        logger.critical("Access denied to webpage")
        return True


    def get_job_links(self):
        csspath = "td.css-1id8hns a"
        wait_for_element_to_load(self.driver, By.CSS_SELECTOR, csspath, timeout=6)
        a_tags = self.driver.find_elements(By.CSS_SELECTOR,csspath)    
        for a in a_tags:
            self.links.append(a.get_attribute('href'))


    @handle_general_exceptions        
    def position(self):
        self.job_title = findelement(self.driver, By.CLASS_NAME, "title_bar_job-name__Qr6Sy","title")
        
    
    @handle_general_exceptions        
    def com_vertical(self):
        self.vertical = findelement(self.driver, By.XPATH,"//td[text()='Vertical']/following-sibling::td","vertical")
        
    
    def get_scrapper(self):
        self.data = {
                "job_id":self.id,
                "job_url": self.job_url,
                "job_title": self.job_title,
                "job_location": self.job_location,
                "salary": self.salary,
                "commitment": self.commitment,
                "job_description": self.job_description,
                "vertical": self.vertical,
                "subvertical": self.subvertical,
                "size": self.size,
                "stage": self.stage,
                "total_equity_funding": self.total_equity_funding,
                "last_funding_date": self.last_funding_date,
                "investors": self.investors,
                "company_location": self.company_location,
                "company_website": self.company_website,
                "company_logo": self.company_logo,
                "company_description": self.company_description,    
                "LinkedIn page": self.linkedin_page,
                }
        logger.info(self.data)
  
    
    def insert_into_dynamodb(self,scraper_data):
        table = self.dynamodb.Table('job_list')
        try:
            table.put_item(
                Item=scraper_data,
                ConditionExpression="attribute_not_exists(job_id)"
                )
            print(f"Data inserted into DynamoDB table: {scraper_data}")
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                logger.debug("job_id already present in database")
        except Exception as e:
            print(f"Error inserting data into DynamoDB: {e}")
