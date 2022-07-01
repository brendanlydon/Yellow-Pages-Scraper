# Yellow-Pages-Scraper
Use Scrapy to pull information on any combination of location and key term from Yellow Pages.
***MUST HAVE SCRAPY AND PYTHON INSTALLED TO USE

This script will build a JSON file and a CSV file containing the following information for any keyword/location pair on https://www.yellowpages.com/.

__Data Pulled from Yellow Pages__
  > __'business_name'__: Official name of business listed on Yellow Pages.<br> 
  __'street_address'__: Official address of business.<br>
  __'address_nickname'__: If available, a localized version of the official address (i.e., "We are located at blah blah blah").<br>
  __'email_address'__: Email address of owner, location, etc. attached to business.<br>
  __'phone_primary'__: Primary phone number of business, owner, etc.<br>
  __'phone_secondary'__: Secondary phone number of business, owner, etc.<br>
  __'website'__: Primary website of business.<br>
  __'general_info'__: General description of business.<br>
  __'hours_open_title'__: TBD<br>
  __'hours_open'__: TBD<br>
  __'payment_options'__: If available, lists specific cards and payment types accepted by business.<br>
  __'industry_searched'__: Industry search term that led to this specific request.<br>
  __'geo_location_searched'__: Geo location search term that led to this specific request.<br>
  __'listing_url'__: URL of specific request.<br>
  
__Script Overview__<br>
> __main.py__<br>Enter search terms for industy and geo_location into lists. Main then runs scrapy CrawlerProcess first to search_results.py and then profile_detail.py to save all data from yellowpages.<br><br>
> __search_results.py__<br>Takes industry/geo_location key pairs and searches yellow pages. This returns a temporary file storing a list of every URL saved from the search, which is then used with profile_detail.py to finalize search.<br><br>
> __profile_detail.py__<br>Goes through list of saved URLs from search_results.py and pulls key information from each page. This data is then saved into a JSON and CSV file, default named to 'output'.<br><br>
> __data_manager.py__<br>Stores xpath dictionary, regex dictionary, and reusable functions for other files. You can also edit the name of the output files by updated the 'output_file' variable on line 5. <br><br>
