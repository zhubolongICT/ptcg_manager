import requests
import codecs
from bs4 import BeautifulSoup


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}


class Pokemon(object):
    def __init__(self, _id, en_name, zht_name, zhs_name, pinyin):
        self.id = _id
        self.en_name = en_name
        self.zht_name = zht_name
        self.zhs_name = zhs_name
        self.pinyin = pinyin
    
    def to_json(self):
        return '''{"id": "%s", "en_name": "%s", "zht_name": "%s", "zhs_name": "%s", "pinyin": "%s"}''' % (
            self.id, self.en_name, self.zht_name, self.zhs_name, self.pinyin)


def downloadAllPokemon():
    r = requests.get("https://bulbapedia.bulbagarden.net/wiki/List_of_Chinese_Pok%C3%A9mon_names", headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    pokemon_list = list()
    for tr in soup.find_all('tr'):
        idx = 0
        attrs = list()
        for td in tr.find_all('td'):
            attrs.append(td.text.rstrip('\r\n'))
        if len(attrs) == 8:
            pokemon_list.append(Pokemon(attrs[0], attrs[2], attrs[3], attrs[4], attrs[5]))
    return pokemon_list


if __name__ == '__main__':
    pokemons = downloadAllPokemon()
    with codecs.open("all_pokemon.csv", mode='w', encoding='utf-8') as fp:
        for pokemon in pokemons:
            fp.write("%s\t%s\t%s\t%s\t%s\n" % (pokemon.id, 
                pokemon.en_name, pokemon.zht_name, pokemon.zhs_name, pokemon.pinyin))
    