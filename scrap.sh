echo "Running pokemon spider..."
scrapy crawl pokemon_spider -o ./output/pokemons.json
echo "Running ability spider..."
scrapy crawl ability_spider -o ./output/abilities.json
echo "Done."
