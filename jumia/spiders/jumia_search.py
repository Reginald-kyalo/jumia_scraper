import scrapy
from jumia.itemloaders import JumiaProductLoader
from jumia.items import JumiaProduct

class JumiaSearchSpider(scrapy.Spider):
    name = "jumia_search"

    custom_settings = {
        'FEEDS': { 'data/%(name)s_%(time)s.csv': { 'format': 'csv',}}
        }

    def start_requests(self):
        keyword_list = ['ipad']
        for keyword in keyword_list:
            jumia_search_url = f'https://www.jumia.co.ke/catalog/?q={keyword}&page=1'
            yield scrapy.Request(url=jumia_search_url, callback=self.parse_search_results, meta={'keyword': keyword, 'page': 1})

    def parse_search_results(self, response):
        page = response.meta['page']
        keyword = response.meta['keyword'] 

        ## Extract Overview Product Data
        search_products = response.css("article.prd._fb.col.c-prd")
         for product in products:
            chocolate = ChocolateProductLoader(item=ChocolateProduct(), selector=product)
            chocolate.add_css('name', "a.product-item-meta__title::text")
            chocolate.add_css('price', 'span.price', re='<span class="price">\n              <span class="visually-hidden">Sale price</span>(.*)</span>')
            chocolate.add_css('url', 'div.product-item-meta a::attr(href)')
            yield chocolate.load_item()
        for product in search_products:
            jumia_product = JumiaProductLoader(item=JumiaProduct(), selector=product)
            jumia_product.add_css('title', "h3.name::text")
            jumia_product.add_css('keyword', keyword)
            jumia_product.add_css('url', "a::attr(href)")
            jumia_product.add_css('current_price', "div.prc::text")
            jumia_product.add_css('image', "div.img-c img::attr(data-src)")
            yield jumia_product.load_item()
            ## Get All Pages
        if page == 1:
            last_page = 10
            for page_num in range(2, int(last_page)):
                jumia_search_url = f'https://www.jumia.co.ke={keyword}&page={page_num}'
                yield scrapy.Request(url=jumia_search_url, callback=self.parse_search_results, meta={'keyword': keyword, 'page': page_num})


        
    

