from scrapy import Spider
from scrapy.loader import ItemLoader
from scrapy_selenium import SeleniumRequest
from ..items import BikeAccessoryItem
from ..web_driver import WebDriver

class BikeAccessoriesSpider(Spider):
    name = 'bike_accessories'
    start_urls = [ 
        "https://mr-bricolage.bg/bg/Instrumenti/Avto-i-veloaksesoari/Veloaksesoari/c/006008012"
    ]
    
    def parse(self, response):
        for product_href in response.css(".product").xpath(".//div[@class='title']//a/@href").getall():
            product_url = response.urljoin(product_href)
            yield SeleniumRequest(
                url=product_url, 
                callback=self.parse_product,
                meta={"product_url": product_url},
                wait_time=3
            )

        next_page = response.css("li.pagination-next a::attr(href)").get()
        if next_page is not None:
            yield response.follow(url=next_page, callback=self.parse)

    def parse_product(self, response):
        for sel in response.css("main"):
            l = ItemLoader(item=BikeAccessoryItem(), selector=sel)
            
            product_url = response.meta["product_url"]
            if len(product_url) == 1:
                product_url = product_url[0]

            l.add_value("product_url", product_url)
            l.add_css("title", ".product-single h1::text")
            l.add_css("price", ".product-single .price p.price::text")
            l.add_css("image_url", ".product-single .row img::attr(src)")
            l.add_css("serial_num", ".product-details .tab-pane#home  span")
            description = sel.css(".product-details .tab-pane#home table td").getall()
            l.add_value("description", description)
                
            # * Initialize Selenium WebDriver
            driver = WebDriver()
            driver.get_stock_availability(product_url)
            stock_availability = driver.stock_availability
            l.add_value("store_stock_info", stock_availability)
            yield l.load_item()
        