import sys
from scrapy.crawler import CrawlerProcess
import search_results as sr
import profile_detail as pd

### Enter search industry and location into industry and geo_location lists below
industry = ['Data Management','SaaS','SEO']
geo_location = ['Exton, PA']

### DO NOT EDIT BELOW
def create_input(lst):
    lst = ';'.join(lst)
    lst = f"'{lst}'"
    return lst

industry = create_input(industry)
geo_location = create_input(geo_location)

process = CrawlerProcess()
crawlers = {
    'search_results' : f'process.crawl(sr.SearchResultsSpider, industry={industry}, geo_location={geo_location})',
    'profile_detail' : f'process.crawl(pd.ProfileDetailSpider)'
}

for crawler in crawlers:
    exec(crawlers[crawler])
    if "twisted.internet.reactor" in sys.modules:
        del sys.modules["twisted.internet.reactor"]
    process.start()