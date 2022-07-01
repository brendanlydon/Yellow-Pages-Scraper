import os
import scrapy
from scrapy.crawler import CrawlerProcess
import data_manager as dm
from time import sleep

class SearchResultsSpider(scrapy.Spider):
    name = 'search_results'
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }

    tmp_format, tmp_loc = dm.stucture_build('json','search_results')
    custom_settings = { 'FEEDS':{tmp_loc : { 'format' : 'json'}}}

    def __init__(self, *args, **kwargs):
        super(SearchResultsSpider, self).__init__(*args, **kwargs)
        self.xp_dict = dm.xpath_dict['search_results']
        self.xp_reg = dm.regex_dict['search_results']

        parameters = ['industry', 'geo_location']
        for param in parameters:
            if not hasattr(self, param):
                continue
        try:
            self.urls = dm.build_url(self.industry, self.geo_location)
        except:
            # Testing this file only
            self.urls = ['https://www.yellowpages.com/search?search_terms=Dog&geo_location_terms=exton%2C+pa']

    def start_requests(self):
        urls = self.urls
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)
    
    def parse(self, response):
        base_url = 'https://www.yellowpages.com'  
        listings = response.xpath(self.xp_dict['listings'])
        for card in listings:
            industry = dm.extract_terms(self.xp_reg['industry'], response.request.url).split('&')[0]
            geo_location = dm.extract_terms(self.xp_reg['geo_location'], response.request.url).split('&')[0]
            listing_url = card.xpath(self.xp_dict['listing_url']).get()
            
            items = {
                'industry' : industry,
                'geo_location' : geo_location,
                'listing_url' : f'{base_url}{str(listing_url)}',
            }

            yield items

        if response.xpath(self.xp_dict['next_page']):
            next_url= response.xpath('next_url').get().replace('&referredBy=UNKNOWN','')
            # go to next page, until no more 'next'
            yield response.follow(next_url, callback=self.parse)
        
# -- main driver --
if __name__ == "__main__" :
    process = CrawlerProcess()
    process.crawl(SearchResultsSpider)
    process.start()