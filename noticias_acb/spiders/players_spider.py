
import scrapy

from noticias_acb.items import TeamItemLoader
from noticias_acb.items import PlayerItemLoader


class AcbSpider(scrapy.Spider):
    name = "players"
    start_urls = ["http://www.acb.com/resulcla.php"]

    def parse(self, response):
        for team in response.css('table.resultados2 tr'):
            # extract basic info
            name = team.css('a.negro::text').extract_first()
            meta = {'name': name}
            
            # get player data for each team
            url_detail = team.css('a.negro::attr(href)').extract_first()
            if url_detail is None:
                continue
            yield response.follow(url_detail, callback=self.parse_detail, meta=meta)
            
    def parse_detail(self, response):
        meta = response.meta
        url = response.css('div#jugadorextrastop a::attr(href)').extract_first()
        yield response.follow(url, callback=self.parse_players, meta=meta)

    def parse_players(self, response):
        meta = response.meta

        for player in response.css('table.plantilla tr'):
            player_name = player.css('td.beige a::attr(href)').extract_first()
            if player_name is None:
                continue
            yield response.follow(player_name, meta=meta, callback=self.parse_player_detail)

    def parse_player_detail(self, response):
        player_name = response.css('td.datojug::text').extract_first()
        twitter = response.css('a font b::text').extract_first()
        team = response.meta['name']

        item = PlayerItemLoader(response=response)
        item.add_value('player_name', player_name)
        item.add_value('twitter', twitter)
        item.add_value('team', team)
        yield item.load_item()