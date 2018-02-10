import json

with open('player_ids.txt', 'a') as ids:
    with open('players.json') as player:
        d = json.load(player)

        for item in d:
            cod = item['cod_player']
            ids.write(cod + '\n')
ids.close()
