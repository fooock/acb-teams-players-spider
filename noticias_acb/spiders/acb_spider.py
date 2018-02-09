
import scrapy

from noticias_acb.items import TeamItemLoader



class AcbSpider(scrapy.Spider):
    name = "acb"
    start_urls = ["http://www.acb.com/resulcla.php"]

    def parse(self, response):
        for team in response.css('td.naranja a.negro::text').extract():

            item = TeamItemLoader(response=response)
            item.add_value('name', team)
            yield item.load_item()
            
        