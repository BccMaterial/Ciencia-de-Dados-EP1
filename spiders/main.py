import scrapy
import re

# Data to get:
# ID x
# URL
# Name x
# Evolutions
# Size in cm x
# Weight in kg x
# Types
# Abilities
# Effectivity

class PokeSpider(scrapy.Spider):
    name = 'pokespider'
    start_urls = ['https://pokemondb.net/pokedex/all']

    def parse(self, response):
        linhas = response.css('table#pokedex > tbody > tr')
        for linha in linhas:
            link = linha.css("td:nth-child(2) > a::attr(href)").get()
            if link:
                yield response.follow(link, self.parser_pokemon)

    def parser_pokemon(self, response):
        pokemon_name = response.css("#main > h1::text").get()

        pokemon_id = response.css("table:nth-child(2) tr:nth-child(1) td strong::text").get()

        pokemon_height = response.css("table:nth-child(2) tr:nth-child(4) td::text").get()
        pokemon_height = float(re.search(r'\d+\.\d+', pokemon_height).group(0)) * 100

        pokemon_weight = response.css("table:nth-child(2) tr:nth-child(5) td::text").get()
        pokemon_weight = float(re.search(r'\d+\.\d+', pokemon_weight).group(0))


        yield {
            "id": int(pokemon_id),
            "name": pokemon_name,
            "height_cm": round(pokemon_height, 2),
            "weight_kg": round(pokemon_weight, 2),
        }
