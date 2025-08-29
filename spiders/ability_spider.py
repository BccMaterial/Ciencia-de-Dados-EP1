import scrapy
import re

class PokeSpider(scrapy.Spider):
    name = 'ability_spider'
    start_urls = ['https://pokemondb.net/ability']

    def parse(self, response):
        lines = response.css('table#abilities > tbody > tr')
        for line in lines:
            url = line.css("td:nth-child(1) a::attr(href)").get()
            name = line.css("td:nth-child(1) a::text").get()
            pokemon_count = int(line.css("td:nth-child(2)::text").get())
            description = line.css("td:nth-child(3)::text").get()
            gen = int(line.css("td:nth-child(4)::text").get())
            yield { 
                "url": url, 
                "name": name, 
                "pokemon_count": pokemon_count, 
                "description": description, 
                "gen": gen 
            }
