import scrapy

class PlayerStatsSpider(scrapy.Spider):
    name = "stats"
    start_urls = ["http://www.acb.com"]

    def parse(self, response):
        with open('player_ids.txt') as ids:
            for id in ids.readlines():
                url = self.start_urls[0] + "/stspartidojug.php?cod_jugador={}".format(id)
                yield scrapy.Request(url.replace('\n', ''), callback=self.parse_player_stats)
        ids.close()

    def parse_player_stats(self, response):
        tr = response.css('table.estadisticas2')

        # stats start at row 2
        
        game = tr.css('tr')[2].css('td a::text').extract_first()
        num_stats = tr.css('tr')[2].css('td::text').extract()

        min_t = num_stats[1]
        pt = num_stats[2]
        t2 = num_stats[3]
        t3 = num_stats[4]
        t1 = num_stats[5]
        tdo = num_stats[6]
        a = num_stats[7]
        br = num_stats[8]
        c = num_stats[9]
        fc = num_stats[10]
        m = num_stats[11]
        f = num_stats[12]
        c = num_stats[13]
        pm = num_stats[14]
        v = num_stats[15]

        yield {'game' : game, 'min': min_t, 'pt': pt, 't2': t2}