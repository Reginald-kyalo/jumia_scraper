from itemloaders.processors import TakeFirst, MapCompose
from scrapy.loader import ItemLoader

class JumiaProductLoader(ItemLoader):

    default_output_processor = TakeFirst()
    current_price_in = MapCompose(lambda x: x.split("KSh")[-1].strip().replace(",", ""))
    url_in = MapCompose(lambda x: 'https://www.jumia.co.ke' + x )
