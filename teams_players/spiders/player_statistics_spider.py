import scrapy

class PlayerStatsSpider(scrapy.Spider):
    name = "stats"
    start_urls = "http://www.acb.com/stspartidojug.php?cod_jugador={}"

    def parse(self, response):
        