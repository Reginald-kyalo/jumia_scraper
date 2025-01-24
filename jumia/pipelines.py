from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class CheckPriceAvailablity:

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        ## check is price present
        if not adapter.get('current_price'):
            raise DropItem(f"Missing price in {item}")
        
class DuplicatesPipeline:

    def __init__(self):
        self.seen_urls = set()

    def process_item(self, item, spider):
        product_url = item['url']
        if product_url in self.seen_urls:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.seen_urls.add(product_url)
            return item