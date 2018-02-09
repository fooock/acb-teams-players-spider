# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst


class TeamItem(scrapy.Item):
    ''' Item for team info'''
    name = scrapy.Field()
    played = scrapy.Field()
    win = scrapy.Field()
    lose = scrapy.Field()
    points_f = scrapy.Field()
    points_l = scrapy.Field()   


class TeamItemLoader(ItemLoader):
    ''' Item loader for NoticiasAcbItem '''
    default_item_class = TeamItem
    
    name_out = TakeFirst()
    played_out = TakeFirst()
    win_out = TakeFirst()
    lose_out = TakeFirst()
    points_f_out = TakeFirst()
    points_l_out = TakeFirst()
