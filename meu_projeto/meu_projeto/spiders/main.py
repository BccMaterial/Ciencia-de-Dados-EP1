import scrapy

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

        abilities = response.css("table.vitals-table tr:contains('Abilities') td a::text").getall()
        abilities_description = response.css("div.grid-row > div:nth-child(1) > p::text").getall()

        yield {
            "pokemon": pokemon_name,
            "habilidades": abilities,
            "desc_habilidades": abilities_description
        }