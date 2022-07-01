import urllib.parse
import re
import os

output_file = 'output'
regex_dict = {
    'search_results':{
        'industry':r'(?<=search_terms=).*(?=&geo_location_terms=)',
        'geo_location':r'(?<=geo_location_terms=).*',
    },
    'profile_detail':{
        
    },
}

xpath_dict = {
    'search_results':{
        'listings':'//*[@class="result"]',
        'listing_url':'.//*[@class="business-name"]/@href',
        'next_page':'//a[contains(@class,"next")]',
        'next_url':'//a[contains(@class,"next")]/@href',
    },
    'profile_detail':{
        'business_name':'//h1[contains(@class, "business-name")]/text()',
        'street_address':'//*[contains(@id, "details-card")]/p[.//span[contains(text(),"Address")]]/text()',
        'address_nickname':'//*[@class="location-description"]/text()',
        'email_address':'//*[@class="email-business"]/@href',
        'phone_primary':'//*[contains(@id, "details-card")]/p[@class="phone"]/text()',
        'phone_secondary':'//*[@class="extra-phones"]/p/span[contains(text(),"(")]/text()',
        'website':'//a[contains(@class, "website-link")]/@href',
        'payment_options':'//*[@class="payment"]/text()',
        'general_info':'//*[@class="general-info"]/text()',
        'hours_open_title':'//*[@class="open-hours"]/div/span/text()',
        'hours_table':'//tr[.//th[@class="day-label"]]/text()',
        'hours_label':'.//th[@class="day-label"]/text()',
        'hours_hours':'.//td[@class="day-hours"]/time/text()',
    },
}

def build_url(key_terms, geo_location):
    geo_location = geo_location.split(';')
    key_terms = key_terms.split(';')

    keys = []
    locs = []
    start_urls = []
    
    for key in key_terms:
        key_search = urllib.parse.quote_plus(key)
        keys.append(key_search)

    for location in geo_location:
        location_search = urllib.parse.quote_plus(location)
        locs.append(location_search)

    for location in locs:
        for key in keys:
            url = f'https://www.yellowpages.com/search?search_terms={key}&geo_location_terms={location}'
            start_urls.append(url)

    return start_urls
    
def extract_terms(regex, url):
    terms = re.search(regex, url).group(0)
    terms = urllib.parse.unquote(terms).replace('+',' ').strip()

    return terms

def remove_file(file_path):
    try:
        os.remove(file_path)
    except OSError:
        pass
    return True

def make_directory(dirName): 
    try:
        os.makedirs(dirName)

    except FileExistsError:
        pass
    return True

def stucture_build(out_frmt, out_name, action=True):
    os.chdir(os.path.dirname(__file__))
    temp_fldr = '.\\tmp'
    out_name = out_name.replace(f'.{out_frmt}','')
    out_loc = f'{temp_fldr}\\{out_name}.{out_frmt}'

    if action:
        make_directory(temp_fldr)
        remove_file(out_loc)

    return out_frmt, out_loc

# -- main driver --
if __name__ == "__main__" :
    pass