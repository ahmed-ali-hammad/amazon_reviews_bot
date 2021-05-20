from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
  
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import json

url = "https://www.amazon.com/"
ASIN = "B07QXV6N1B"


options = webdriver.ChromeOptions()  # initializing the chrome options
# options.add_argument("--headless")   # to run in the background
options.add_argument("--incognito ") # to run in incognito mode
driver = webdriver.Chrome('chromedriver.exe', options = options)

class JsonReport: # this class is used to save the scraped data to an external json file
    def __init__(self, data):
        self.data = data

    def json_create(self):
        print('saving the scraped data to an external file')
        with open ("scraped_data.json", "w") as f:
            json.dump(self.data, f , indent = 4)




class AmazonReviewsScraper: # this class is used to scrape the data
    def __init__(self, ASIN, url):
        self.search_url = url + "/product-reviews/" + ASIN

    def run (self): # this method is responsible for excuring all the other methods inside the class
        print("running the app")
        driver.get(self.search_url)
        reviews = self.get_reviews()
        # driver.quit()
        return reviews

 
    def get_reviews(self):
        condition = True
        data = [] 
        while condition:
            reviews = driver.find_elements_by_xpath("//div[@class='a-section celwidget']")

            for count, review in enumerate(reviews):
                # review_title = review.find_element_by_xpath(".//a[@data-hook ='review-title']/span").text
                # review_body = review.find_element_by_xpath(".//span[@data-hook ='review-body']/span").text
                # star_rating = review.find_element_by_xpath(".//span[@class ='a-icon-alt']").get_attribute("innerHTML")
                # buyer_name = review.find_element_by_xpath(".//span[@class ='a-profile-name']").text
                # buyer_profile = review.find_element_by_xpath(".//a[@class ='a-profile']").get_attribute('href')

                review_title = WebDriverWait(review, 15).until(
                                        EC.presence_of_element_located((By.XPATH, ".//a[@data-hook ='review-title']/span"))).text

                review_body = WebDriverWait(review, 15).until(
                                        EC.presence_of_element_located((By.XPATH, ".//span[@data-hook ='review-body']/span"))).text

                star_rating = WebDriverWait(review, 15).until(
                                        EC.presence_of_element_located((By.XPATH, ".//span[@class ='a-icon-alt']"))).get_attribute("innerHTML")
                
                buyer_name = WebDriverWait(review, 15).until(
                                        EC.presence_of_element_located((By.XPATH, ".//span[@class ='a-profile-name']"))).text
                
                buyer_profile = WebDriverWait(review, 15).until(
                                        EC.presence_of_element_located((By.XPATH, ".//a[@class ='a-profile']"))).get_attribute('href')




                review_data = { "review #" + str(count+1):[
                        {"Title": review_title},
                        {"Body":review_body}, 
                        {"Rating":star_rating}, 
                        {"Buyer":buyer_name},
                        {"Buyer Profile":buyer_profile}
                        ]}
                data.append(review_data)
            try: 
                new_url = driver.find_element_by_xpath(".//li[@class ='a-last']/a").get_attribute('href')
                print(new_url)
                print('sucess loop')
                driver.get(new_url)
            except: 
                print('exit loop')
                condition = False
            if len(reviews) == 1:
                condition = False
            condition = False
        return data



if __name__ == '__main__': 
    scraped_data = AmazonReviewsScraper(ASIN, url)
    data = scraped_data.run()
    json_output = JsonReport(data)
    json_output.json_create()





