import mysql.connector
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class CheckPriceAvailablity:

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        ## check is price present
        if not adapter.get('current_price'):
            raise DropItem(f"Missing price in {item}")
        return item

class DuplicatesPipeline:

    def __init__(self):
        self.seen_urls = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        product_url = adapter.get('url')

        # Ensure the product has a valid URL
        if not product_url:
            raise DropItem(f"Missing URL in {item}")
        if product_url in self.seen_urls:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.seen_urls.add(product_url)
            return item

class MySQLNoDuplicatesPipeline:

    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'scraper',
            password = 'scraper',
            database = 'scraperdb'
        )

        ## Create cursor, used to execute commands
        self.cur = self.conn.cursor()
        
        ## Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS jumia(
            id INT NOT NULL AUTO_INCREMENT, 
            keyword TEXT(255) NOT NULL, 
            title TEXT(255) NOT NULL, 
            url TEXT(255) NOT NULL UNIQUE, 
            current_price INT NOT NULL, 
            image TEXT(255) NOT NULL, 
            PRIMARY KEY (id)
        )
        """)

    def process_item(self, item, spider):
        ## Define insert statement with INSERT IGNORE to avoid duplicates
        self.cur.execute("""
            INSERT IGNORE INTO jumia (keyword, title, url, current_price, image)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            item["keyword"],
            item["title"],
            item["url"],  # Ensure URL is in string format
            item["current_price"],
            item["image"]
        ))
    
        ## Log if the item is being ignored (for debugging purposes)
        if self.cur.rowcount == 0:
            spider.logger.warn("Item already in database (ignored): %s" % item['url'])
    
    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.conn.close()

