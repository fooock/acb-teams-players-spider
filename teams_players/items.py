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
    points_w = scrapy.Field()
    points_l = scrapy.Field()  
    players = scrapy.Field() 


class TeamItemLoader(ItemLoader):
    ''' Item loader for NoticiasAcbItem '''
    default_item_class = TeamItem

    name_out = TakeFirst()
    played_out = TakeFirst()
    win_out = TakeFirst()
    lose_out = TakeFirst()
    points_w_out = TakeFirst()
    points_l_out = TakeFirst()

class PlayerItem(scrapy.Item):
    player_name = scrapy.Field()
    twitter = scrapy.Field()
    team = scrapy.Field()
    photo = scrapy.Field()
    country = scrapy.Field()
    birth_date = scrapy.Field()
    position = scrapy.Field()
    height = scrapy.Field()

class PlayerItemLoader(ItemLoader):
    ''' Item loader for NoticiasAcbItem '''
    default_item_class = PlayerItem

    player_name_out = TakeFirst()
    twitter_out = TakeFirst()
    team_out = TakeFirst()
    photo_out = TakeFirst()
    country_out = TakeFirst()
    birth_date_out = TakeFirst()
    position_out = TakeFirst()
    height_out = TakeFirst()