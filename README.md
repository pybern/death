# death

Scrapy script to crawl executed offenders from the Texas Justice Department. 

This project also includes esWrapper which transforms the data and uploads it to the ELK stack. 

Run scrapy crawl death -o info.json -t to start crawler and download the data in current directory


#scrapy

The script crawls the main table and each of its links to return meaningful information. 

In any case where the link leads to a no information or image page. It will return blank. 

To view more about the page. The link of these images will also be extracted for references. 

