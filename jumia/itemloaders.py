from itemloaders.processors import TakeFirst, MapCompose
from scrapy.loader import ItemLoader

class JumiaProductLoader(ItemLoader):

    default_output_processor = TakeFirst()
    price_in = MapCompose(lambda x: x.split("Ksh")[-1])
    url_in = MapCompose(lambda x: 'https://www.jumia.co.ke' + x )
