import scrapy
from scrapy.loader import ItemLoader
from ..items import BikeAccessoryItem

# ! Details to scrape
# * Title
# * Price
# * Image
# * Description
# ? Availability in stores
# ? Format the price in F2 numeric

class BikeAccessoriesSpider(scrapy.Spider):
    name = 'bike_accessories'
    start_urls = [ 
        "https://mr-bricolage.bg/bg/Instrumenti/Avto-i-veloaksesoari/Veloaksesoari/c/006008012"
    ]

    def parse(self, response):
        for product_href in response.css(".product").xpath(".//div[@class='title']//a/@href").getall():
            product_url = response.urljoin(product_href)
            yield scrapy.Request(url=product_url, callback=self.parse_product)
            
        next_page = response.css("li.pagination-next a::attr(href)").get()
        if next_page is not None:
            yield response.follow(url=next_page, callback=self.parse)

    def parse_product(self, response):
        for sel in response.css(".product-single"):
            l = ItemLoader(item=BikeAccessoryItem(), selector=sel)
            l.add_css("title", "h1::text")
            l.add_css("price", ".price p.price::text")
            l.add_css("image_url", ".row .owl-item img::attr(src)")
            #description

            yield l.load_item()