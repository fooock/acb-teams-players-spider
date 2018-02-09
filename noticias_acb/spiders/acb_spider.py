
import scrapy

from noticias_acb.items import TeamItemLoader


class AcbSpider(scrapy.Spider):
    name = "acb"
    start_urls = ["http://www.acb.com/resulcla.php"]

    def parse(self, response):
        for team in response.css('table.resultados2 tr'):
            item = TeamItemLoader(response=response)
            item.add_value('name', team.css('a.negro::text').extract_first())
            item.add_value('played', team.css('td::text')[2].extract())
            item.add_value('win', team.css('td::text')[3].extract())
            item.add_value('lose', team.css('td::text')[4].extract())
            item.add_value('points_w', team.css('td::text')[5].extract())
            item.add_value('points_l', team.css('td::text')[6].extract())
            yield item.load_item()
            
        