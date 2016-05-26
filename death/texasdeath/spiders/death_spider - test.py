from urlparse import urljoin
import scrapy
from texasdeath.items import DeathItem
 
 
class DeathSpider(scrapy.Spider):
    name = "deatht"
    allowed_domains = ["tdcj.state.tx.us"]
    start_urls = [
        "https://www.tdcj.state.tx.us/death_row/dr_executed_offenders.html"
    ]
    def parse(self, response):
        sites = response.xpath('//table/tbody/tr')
        for site in sites:
            item = DeathItem()
            item['Mid'] = site.xpath('td[1]/text()').extract()
            item['firstName'] = site.xpath('td[5]/text()').extract()
            item['lastName'] = site.xpath('td[4]/text()').extract()
            item['Age'] = site.xpath('td[7]/text()').extract()
            item['Date'] = site.xpath('td[8]/text()').extract()
            item['Race'] = site.xpath('td[9]/text()').extract()
            item['County'] = site.xpath('td[10]/text()').extract()
            
            url = urljoin(response.url, site.xpath("td[2]/a/@href").extract_first())
            urlLast = urljoin(response.url, site.xpath("td[3]/a/@href").extract_first())
 
            if url.endswith(("jpg","no_info_available.html")):
                item['Desc'] = url
                if urlLast.endswith("no_last_statement.html"):
                    item['Message'] = "No last statement"
                    yield item
                else:
                    request = scrapy.Request(urlLast, meta={"item" : item}, callback =self.parse_details2)
                    yield request
            else:        
                request = scrapy.Request(url, meta={"item": item,"urlLast" : urlLast}, callback=self.parse_details)
                yield request
 
    def parse_details(self, response):
        item = response.meta["item"]
        urlLast = response.meta["urlLast"]
        item['Desc'] = response.xpath("//*[@id='body']/p[3]/text()").extract()
        if urlLast.endswith("no_last_statement.html"):
            item["Message"] = "No last statement"
            return item
        else:
            request = scrapy.Request(urlLast, meta={"item": item}, callback=self.parse_details2)
            return request
 
    def parse_details2(self, response):
        item = response.meta["item"]
        item['Message'] = response.xpath("//div/p[contains(., 'Last Statement:')]/following-sibling::node()/descendant-or-self::text()").extract()
        return item
 