import scrapy
import os
from jumia.itemloaders import JumiaProductLoader
from jumia.items import JumiaProduct
from urllib.parse import urlencode

class IV_JumiaSpider(scrapy.Spider):
    name = "IV_jumia_spider"
    start_urls = ["https://www.jumia.co.ke"]

    def __init__(self, keyword=None, *args, **kwargs):
       super(IV_JumiaSpider, self).__init__(*args, **kwargs)
       self.keyword = keyword
        
    def start_requests(self):
        if not self.keyword:
            self.logger.error("No keyword provided")
            return
        for page in range(31, 41):
            jumia_search_url = f'https://www.jumia.co.ke/catalog/?q={self.keyword}&page={page}'
            payload = {
                'api_key': os.getenv("SCRAPINGBEE_API_KEY"),
                'url': jumia_search_url,
                'render_js': 'false'
            }
            proxy_url = 'https://app.scrapingbee.com/api/v1?' + urlencode(payload)
            yield scrapy.Request(
                url=proxy_url, 
                callback=self.parse_search_results, 
                meta={'keyword': self.keyword, 'page': 1}
                )
    def parse_search_results(self, response):
        keyword = response.meta['keyword'] 
        self.logger.debug(f"Parsing URL: {response.url}")
        ## Extract Overview Product Data
        search_products = response.css("article.prd._fb.col.c-prd")
        if not search_products:
            self.logger.info(f"No products found on page {response.meta['page']} for keyword: {response.meta['keyword']}")
            return  # Stop processing if no products are found
        for product in search_products:
            jumia_product = JumiaProductLoader(item=JumiaProduct(), selector=product)
            jumia_product.add_css('title', "h3.name::text")
            jumia_product.add_css('keyword', keyword)
            jumia_product.add_css('url', "a:nth-of-type(2)::attr(href)")
            jumia_product.add_css('current_price', "div.prc::text")
            jumia_product.add_css('image', "div.img-c img::attr(data-src)")
            yield jumia_product.load_item()