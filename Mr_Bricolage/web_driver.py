import os
from scrapy import Selector
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC

class WebDriver:
        stock_availability = []

        def __init__(self):
                os.environ["PATH"] += os.pathsep + r'./chromedriver.exe'
                self.driver = Chrome()

        def get_stock_availability(self, product_url):
                self.driver.get(product_url)
                stock_button = self.driver.find_element_by_css_selector(".js-pickup-in-store-button")
                stock_button.click()
                WebDriverWait(self.driver, 3).until(
                        EC.presence_of_element_located([By.CSS_SELECTOR, ".pickup-store-list-entry"]))
                self.parse_stock_availability(self.driver.page_source)
                self.driver.close()

        def parse_stock_availability(self, body):
                sel = Selector(text=body)
                store_list = sel.css(".store-navigation .js-pickup-store-list")
                for store_data in store_list.css(".pickup-store-list-entry"):
                        store_info = store_data.css(".js-select-store-label")
                        store_name = store_info.css(".pickup-store-info .pickup-store-list-entry-name").get()
                        store_address = store_info.css(".pickup-store-info .pickup-store-list-entry-address").get()
                        store_city = store_info.css(".pickup-store-info .pickup-store-list-entry-city").get()  
                        stock_info = store_info.css(".store-availability .available").get()
                        result = [store_name, store_address, store_city, stock_info]
                        self.stock_availability += result
