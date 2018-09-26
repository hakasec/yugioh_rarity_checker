""" Functions for scraping rarity data from the Yu-Gi-Oh wikia. """

import requests
from bs4 import BeautifulSoup

TCG_RARITY = (
    "COMMON",
    "SHORT PRINT",
    "SUPER SHORT PRINT",
    "RARE",
    "GOLD RARE",
    "SUPER RARE",
    "HOLOFOIL RARE",
    "ULTRA RARE",
    "SECRET RARE",
    "GOLD SECRET RARE",
    "ULTRA SECRET RARE",
    "SECRET ULTRA RARE",
    "PRISMATIC SECRET RARE",
    "PARALLEL COMMON",
    "PARALLEL RARE",
    "SUPER PARALLEL RARE",
    "ULTRA PARALLEL RARE",
    "DUEL TERMINAL PARALLEL COMMON",
    "DUEL TERMINAL RARE PARALLEL RARE",
    "DUEL TERMINAL SUPER PARALLEL RARE",
    "DUEL TERMINAL ULTRA PARALLEL RARE",
    "DUEL TERMINAL SECRET PARALLEL RARE",
    "ULTIMATE RARE",
    "GHOST RARE",
)

def get_page(url: str) -> BeautifulSoup:
    """ Returns BeautifulSoup for page at url. """
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception(f'Failed to get page at {url}')
    return BeautifulSoup(r.text, 'html.parser')


def get_english_tcg_table(page: BeautifulSoup) -> BeautifulSoup:
    """ Returns the English TCG table on a given page. """
    card_tables = page.find_all(class_='cardtablespanrow')
    for table in card_tables:
        if 'TCG sets' in table.get_text():
            return table.table.find_all('table')[-1]


def get_table_header(table: BeautifulSoup) -> list:
    """ Return table headers. """
    headers = []
    for th in table.find_all('th', recursive=True):
        headers.append(th.get_text().strip())
    return headers


def get_table_data(table: BeautifulSoup) -> list:
    """ Return table data. """
    data = []
    for tr in table.find_all('tr'):
        row = []
        for td in tr.find_all('td'):
            row.append(td.get_text().strip())
        if row:
            data.append(row)
    return data