
import scrapy

from noticias_acb.items import TeamItemLoader


class AcbSpider(scrapy.Spider):
    name = "acb"
    start_urls = ["http://www.acb.com/resulcla.php"]
    players_url = "http://www.acb.com/plantilla.php{}"

    def parse(self, response):
        for team in response.css('table.resultados2 tr'):
            # extract basic info
            name = team.css('a.negro::text').extract_first()
            played = team.css('td::text')[2].extract()
            win = team.css('td::text')[3].extract()
            lose = team.css('td::text')[4].extract()
            points_w = team.css('td::text')[5].extract()
            points_l = team.css('td::text')[6].extract()

            meta = {'name': name, 'played': played, 'win' : win, 'loses': lose, 'points_w': points_w, 'points_l': points_l}
            
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
        players = []

        for player in response.css('table.plantilla tr'):
            player_name = player.css('td.beige a::text').extract_first()
            if player_name is None:
                continue
            # add each player
            players.append(player_name)

        item = TeamItemLoader(response=response)
        item.add_value('name', response.meta['name'])
        item.add_value('played', response.meta['played'])
        item.add_value('win', response.meta['win'])
        item.add_value('lose', response.meta['loses'])
        item.add_value('points_w', response.meta['points_w'])
        item.add_value('points_l', response.meta['points_l'])
        item.add_value('players', players)
        yield item.load_item()