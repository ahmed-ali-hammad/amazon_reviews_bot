from selenium import webdriver
import json

url = "https://www.amazon.com/"
ASIN = "B07QXV6N1B"


options = webdriver.ChromeOptions()  # initializing the chrome options
options.add_argument("--headless")   # to run in the background
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

            for review in reviews:
                try:
                    review_title = review.find_element_by_xpath(".//a[@data-hook ='review-title']/span").text
                except:
                    review_title = review.find_element_by_xpath(".//span[@data-hook ='review-title']/span").text
                review_body = review.find_element_by_xpath(".//span[@data-hook ='review-body']/span").text
                star_rating = review.find_element_by_xpath(".//span[@class ='a-icon-alt']").get_attribute("innerHTML")
                buyer_name = review.find_element_by_xpath(".//span[@class ='a-profile-name']").text
                try:
                    buyer_profile = review.find_element_by_xpath(".//a[@class ='a-profile']").get_attribute('href')
                except: 
                    buyer_profile = "Not Available"

                review_data = [
                        {"Title": review_title},
                        {"Body": review_body}, 
                        {"Rating": star_rating}, 
                        {"Buyer": buyer_name},
                        {"Buyer Profile": buyer_profile}
                        ]
                data.append(review_data)
            try: 
                new_url = driver.find_element_by_xpath(".//li[@class ='a-last']/a").get_attribute('href')
                print('sucess loop')
                driver.get(new_url)
            except: 
                print('LAST PAGE')
                condition = False
        return data



if __name__ == '__main__': 
    scraped_data = AmazonReviewsScraper(ASIN, url)
    data = scraped_data.run()
    json_output = JsonReport(data)
    json_output.json_create()





