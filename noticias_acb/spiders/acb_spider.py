
import scrapy

from noticias_acb.items import TeamItemLoader


class AcbSpider(scrapy.Spider):
    name = "acb"
    start_urls = ["http://www.acb.com/resulcla.php"]

    def parse(self, response):
        for team in response.css('table.resultados2 tr'):
            item = TeamItemLoader(response=response)
            item.add_value('name', team.css('a.negro::text').extract_first())
            item.add_value('played', team.css('td.grisclaro::text').extract_first())
            yield item.load_item()
            
        