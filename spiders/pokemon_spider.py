import scrapy
import re

class PokeSpider(scrapy.Spider):
    name = 'pokemon_spider'
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

        abilities_urls = response.css("table.vitals-table tr:contains('Abilities') td a::attr(href)").getall()

        pokemon_types = response.css("table:nth-child(2) tr:nth-child(2) td a::attr(href)").getall()

        effectiveness = self.parse_effectiveness(response)

        evolutions = self.parse_evolution(response)

        yield {
            "id": int(pokemon_id),
            "variant": 0,
            "name": pokemon_name,
            "types": pokemon_types,
            "height_cm": round(pokemon_height, 2),
            "weight_kg": round(pokemon_weight, 2),
            "effectiveness": effectiveness,
            "url": response.request.url,
            "abilities": abilities_urls,
            "evolution": evolutions
        }

    #def parse_evolution(self, response):
        #evolutions_names = response.css("div.infocard-list-evo > div.infocard a.ent-name::text").getall()
        #return evolutions_names

    def parse_evolution(self, response):#Retorna uma lista de objetos
        evolutions_list = []
        evolutions_names = response.css("div.infocard-list-evo a.ent-name::text").getall()
        evolutions_level_requirements = response.css("div.infocard-list-evo small::text").getall()
        evolutions_item_requirements  = response.css("div.infocard-list-evo span.infocard-arrow a::text").getall()

        for name, level, item in zip(evolutions_names, evolutions_level_requirements, evolutions_item_requirements ):
            evolutions_list.append({
                "name": name,
                "requirements": {
                    "Evolution level": level,
                    "Evolution item": item
            }
        })
        return evolutions_list            
            
    def parse_effectiveness(self, response):
        effectiveness_keys = response.css("table.type-table.type-table-pokedex th a::attr(href)").getall()
        value_regex = r'type-fx-cell\stype-fx-(\d+)'
        effectiveness_values = [
            float(re.search(value_regex, value).group(1)) / 100 for value 
            in response.css("table.type-table.type-table-pokedex td").xpath("@class").extract()
        ]
        return dict(zip(effectiveness_keys, effectiveness_values))
    
    
    
