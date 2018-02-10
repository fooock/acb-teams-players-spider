
import scrapy
import urllib.parse as urlparse

from teams_players.items import TeamItemLoader
from teams_players.items import PlayerItemLoader


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

        url_parse = urlparse.urlparse(response.url) 
        cod_team = urlparse.parse_qs(url_parse.query)['cod_equipo']
        meta['cod_team'] = cod_team

        for player in response.css('table.plantilla tr'):
            player_name = player.css('td.beige a::attr(href)').extract_first()
            if player_name is None:
                continue
            yield response.follow(player_name, meta=meta, callback=self.parse_player_detail)

    def parse_player_detail(self, response):
        player_name = response.css('td.datojug::text').extract_first()
        twitter = response.css('a font b::text').extract_first()
        team = response.meta['name']
        photo = response.css('div#portadaizq img::attr(src)').extract_first()

        personal = response.css('div#portadadertop tr')[1].css('td.datojug::text').extract_first()
        data = personal.split(',')
        country = data[0].strip()
        birth_date = data[len(data) - 1].strip()

        position = response.css('div#portadadertop tr')[2].css('td.datojug::text').extract_first().split('|')[0].strip()
        height = response.css('div#portadadertop tr')[2].css('td.datojug::text').extract_first().split('|')[1].strip()
        
        url_parse = urlparse.urlparse(response.url) 
        cod_player = urlparse.parse_qs(url_parse.query)['id']

        # player statistics

        item = PlayerItemLoader(response=response)
        item.add_value('player_name', player_name)
        item.add_value('twitter', twitter)
        item.add_value('team', team)
        item.add_value('photo', photo)
        item.add_value('country', country)
        item.add_value('birth_date', birth_date)
        item.add_value('position', position)
        item.add_value('height', height)
        item.add_value('cod_team', response.meta['cod_team'])
        item.add_value('cod_player', cod_player)
        yield item.load_item()