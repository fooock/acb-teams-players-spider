# Team and player info
Data from [acb.com](http://www.acb.com)

## Teams

```
scrapy crawl teams -o teams.json -t json
```

## Players

```
scrapy crawl players -o players.json -t json
```

## Stats
Generate the player ids file using the script `extract_player_id.py` before execute the crawler

```
scrapy crawl stats -o stats.json -t json
```

See [teams.json](teams.json), [stats.json](stats.json) or [players.json](players.json) for a structure reference 