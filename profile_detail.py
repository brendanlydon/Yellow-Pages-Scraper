import os
import scrapy
from scrapy.crawler import CrawlerProcess
import data_manager as dm
from time import sleep
import json

output_loc = dm.output_file
output_csv = f'{output_loc}.csv'
output_json = f'{output_loc}.json'

class ProfileDetailSpider(scrapy.Spider):
    name = 'search_results'
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }

    custom_settings = { 
        'FEEDS':{
            output_csv:{'format' : 'csv'},
            output_json:{'format' : 'json'},
        }
    }

    def __init__(self, *args, **kwargs):
        super(ProfileDetailSpider, self).__init__(*args, **kwargs)
        self.xp_dict = dm.xpath_dict['profile_detail']
        self.xp_reg = dm.regex_dict['profile_detail']

        self.tmp_format, self.tmp_loc = dm.stucture_build('json','search_results', action=False)
        dm.remove_file(output_csv)
        dm.remove_file(output_json)

    def start_requests(self):
        with open(self.tmp_loc) as file:
            data = json.load(file)
            for d in data:
                self.url = d['listing_url']
                self.industry = d['industry']
                self.geo_location = d['geo_location']
                yield scrapy.Request(self.url, callback=self.parse)

        dm.remove_file(self.tmp_loc)
    
    def parse(self, response):
        business_name = response.xpath(self.xp_dict['business_name']).get()
        street_address = response.xpath(self.xp_dict['street_address']).get()
        address_nickname = response.xpath(self.xp_dict['address_nickname']).get()
        email_address = response.xpath(self.xp_dict['email_address']).get()
        try:
            email_address = email_address.replace('mailto:','')
        except:
            pass
        phone_primary = response.xpath(self.xp_dict['phone_primary']).get()
        phone_secondary = response.xpath(self.xp_dict['phone_secondary']).get()
        website = response.xpath(self.xp_dict['website']).get()
        payment_options = response.xpath(self.xp_dict['payment_options']).get()
        general_info = response.xpath(self.xp_dict['general_info']).get()
        hours_open_title = response.xpath(self.xp_dict['hours_open_title']).get()
        hours_open = ''
        hours_table = response.xpath(self.xp_dict['hours_table'])
        for h in hours_table:
            hours_label = h.xpath(self.xp_dict['hours_label']).get()
            hours_hours = h.xpath(self.xp_dict['hours_hours']).get()
            hours_row = f'{hours_label} {hours_hours}'
            if len(hours_open) == 0:
                hours_open = hours_row
            else:
                hours_open = f'{hours_open}\n{hours_row}'
        
        items = {
            'business_name' : business_name,
            'street_address' : street_address,
            'address_nickname' : address_nickname,
            'email_address' : email_address,
            'phone_primary' : phone_primary,
            'phone_secondary' : phone_secondary,
            'website' : website,
            'hours_open_title': hours_open_title,
            'hours_open': hours_open,
            'payment_options' : payment_options,
            'general_info' : general_info,
            'industry_searched' : self.industry,
            'geo_location_searched' : self.geo_location,
        }
        yield items
        
# -- main driver --
if __name__ == "__main__" :
    process = CrawlerProcess()
    process.crawl(ProfileDetailSpider)
    process.start()