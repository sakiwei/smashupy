import csv
import requests
from lxml import html

url = 'https://smashup.fandom.com/wiki/Category:Factions'
r = requests.get(url)

# pass content
tree = html.fromstring(r.content)
wiki_tables = tree.xpath('//*[@id="mw-content-text"]/div[@class="mw-parser-output"]/table[@class="wikitable"]')

def get_first(iterable, default=None):
    if iterable:
        for item in iterable:
            return item
    return default

with open('smashup_db.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["name", "icon", "description", "wiki_link"])
    for table in wiki_tables:
        rows = table.xpath('tbody/tr')
        index = 0
        for tableRow in rows:
            if index == 0:
                index += 1
            else:
                if tmp := get_first(tableRow.xpath('td[1]/a/text()')) : name = tmp.strip()
                if tmp := get_first(tableRow.xpath('td[2]/div/figure/a/@href')) : image = tmp.strip()
                if tmp := get_first(tableRow.xpath('td[3]/text()')) :desc = tmp.strip()
                wiki_link = 'https://smashup.fandom.com/' + get_first(tableRow.xpath('td[1]/a/@href'))
                writer.writerow([name, image, desc, wiki_link])
