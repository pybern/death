
#removed, items migrated to spider//from death.items import DeathItem
#items
from urlparse import urljoin
import scrapy
from scrapy.loader import ItemLoader
from texasdeath.items import DeathItem

class DeathSpider(scrapy.Spider):
    name = "tdeath"
    allowed_domains = ["tdcj.state.tx.us"]
    start_urls = [
        "https://www.tdcj.state.tx.us/death_row/dr_executed_offenders.html"
    ]


    def parse(self, response):
        sites = response.xpath('//table/tbody/tr')
        for site in sites:

            url = urljoin(response.url, site.xpath("td[2]/a/@href").extract_first())
            urlLast = urljoin(response.url, site.xpath("td[3]/a/@href").extract_first())
            item = DeathItem()
            loader = ItemLoader(item,selector=site)
            loader.add_xpath('Mid','td[1]/text()')
            loader.add_xpath('firstName','td[5]/text()')
            loader.add_xpath('lastName','td[4]/text()')
            loader.add_xpath('Date','td[8]/text()')
            loader.add_xpath('Race','td[9]/text()')
            loader.add_xpath('County','td[10]/text()')
            loader.add_xpath('Age','td[7]/text()')
            loader.add_value('OILink',url)
            loader.add_value('OLastStatement',urlLast)

 
            if url.endswith(("jpg","no_info_available.html")):
                loader.add_value('Description',u'')
                loader.add_value('Education ',u'')
                if urlLast.endswith("no_last_statement.html"):
                    loader.add_value('Message',u'')
                    yield loader.load_item()
                else:
                    request = scrapy.Request(urlLast, meta={"item" : loader.load_item()}, callback =self.parse_details2)
                    yield request
            else:        
                request = scrapy.Request(url, meta={"item": loader.load_item(),"urlLast" : urlLast}, callback=self.parse_details)
                yield request
 
    def parse_details(self, response):

        item = response.meta["item"]
        urlLast = response.meta["urlLast"]

        loader = ItemLoader(item,response=response)
        loader.add_xpath("Description","//*[@id='body']/p[3]/text()")
        loader.add_xpath("Education","//td[. = 'Education Level (Highest Grade Completed)']/following-sibling::td[1]/text()")

        if urlLast.endswith("no_last_statement.html"):
            loader.add_value('Message',u'')
            return loader.load_item()
        else:
            request = scrapy.Request(urlLast, meta={"item": loader.load_item()}, callback=self.parse_details2)
            return request
 
    def parse_details2(self, response):
        item = response.meta["item"]
        loader = ItemLoader(item,response=response)
        loader.add_xpath("Message","//*[contains(., 'Last Statement:')]/following-sibling::p/text()")
        loader.add_xpath("Message","//*[contains(., 'Last Statement:')]/following-sibling::p/span/text()")
        return loader.load_item()
