import argparse
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import defer
from jumia.spiders.I_jumia_spider import I_JumiaSpider
from jumia.spiders.II_jumia_spider import II_JumiaSpider
from jumia.spiders.III_jumia_spider import III_JumiaSpider
from jumia.spiders.IV_jumia_spider import IV_JumiaSpider
from jumia.spiders.V_jumia_spider import V_JumiaSpider

parser = argparse.ArgumentParser(description="Run multiple Scrapy spiders.")
parser.add_argument('keyword', type=str, help='Keyword to search for eg: Ipad')
args = parser.parse_args()

runner = CrawlerRunner(get_project_settings())


runner.crawl(I_JumiaSpider, args.keyword)
runner.crawl(II_JumiaSpider, args.keyword)
runner.crawl(III_JumiaSpider, args.keyword)
runner.crawl(IV_JumiaSpider, args.keyword)
runner.crawl(V_JumiaSpider, args.keyword)

d = runner.join()

# Once all crawls are finished, exit
d.addCallback(lambda _: print("All spiders have finished crawling!"))