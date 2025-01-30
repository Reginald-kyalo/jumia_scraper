import os
import time
BOT_NAME = 'jumia'

SPIDER_MODULES = ['jumia.spiders']
NEWSPIDER_MODULE = 'jumia.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
SCRAPINGANT_API_KEY = os.getenv("SCRAPINGANT_API_KEY")
SCRAPINGBEE_API_KEY = os.getenv("SCRAPINGBEE_API_KEY")

LOG_LEVEL = 'DEBUG'
LOG_ENABLED = True
LOG_FILE = f'logs/spider_log_{time.strftime("%Y%m%d_%H%M%S")}.log'
TELNETCONSOLE_ENABLED = True

FEEDS = {
    'data/%(name)s/%(name)s_%(time)s.jsonl': {
        'format': 'jsonlines',
        }
}

SPIDER_MIDDLEWARES = {
    'jumia.middlewares.SpiderTimingMiddleware': 543, 
}

#DOWNLOADER_MIDDLEWARES = {
#   'jumia.middlewares.ScrapingAntMiddleware': 543, 
#   'jumia.middlewares.ScrapingBeeMiddleware': 543,
#}

ITEM_PIPELINES = {
    'jumia.pipelines.DuplicatesPipeline': 100,
    'jumia.pipelines.CheckPriceAvailablity': 200,
}

# Max Concurrency On ScrapeOps Proxy Free Plan is 1 thread

HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 3600  # Cache for 1 hour
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = [500, 502, 503, 504, 400, 403, 404, 408]

RETRY_ENABLED = True
RETRY_TIMES = 2  # Limit retries to 2
DOWNLOAD_TIMEOUT = 15  # Set a timeout of 15 seconds

CONCURRENT_REQUESTS = 5
CONCURRENT_REQUESTS_PER_DOMAIN = 5
DOWNLOAD_DELAY = 0.25

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_DEBUG = True