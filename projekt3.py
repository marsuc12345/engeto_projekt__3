"""
projekt: třetí projekt do Engeto Online Python Akademie
author: Marek Suchanek
email: marsuc@seznam.cz
"""


import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import pprint
import csv


def main():
    link = "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=1&xnumnuts=1100"
    output = "projekt3_vystup.csv"
    save_as_csv(get_data(link), output)
    pprint.pprint(get_data(link), width=900)


def get_odkazy_obci(url) -> list:
    """Funkce vytvoří list s odkazy na detaily jednotlivých obcí"""
    req_obce = requests.get(url)
    soup_obce = bs(req_obce.text, "html.parser")
    nalezene_odkazy = []
    for a_elem in soup_obce.find_all("a"):
        href = urljoin(url, a_elem["href"])
        if len(href) > 70 and href not in nalezene_odkazy:
            nalezene_odkazy.append(href)
    return nalezene_odkazy


def get_cisla_obci(url) -> list:
    """Funkce vytvoří list s čísly obcí daného okresu"""
    req_obce = requests.get(url)
    soup_obce = bs(req_obce.text, "html.parser")
    nalezene_cisla = []
    for elem in soup_obce.find_all("td", {"headers": ["t1sb1", "t2sb1", "t3sb1"]}):
        text = elem.text
        nalezene_cisla.append(text)
    return nalezene_cisla


def get_nazvy_obci(url) -> list:
    """Funkce vytvoří list s názvy obcí daného okresu"""
    req_obce = requests.get(url)
    soup_obce = bs(req_obce.text, "html.parser")
    nalezene_obce = []
    for elem in soup_obce.find_all("td", {"class": "overflow_name"}):
        text = elem.text
        nalezene_obce.append(text)
    return nalezene_obce


def get_data(url) -> list:
    """Funkce vytvoří finální list s veškerými hledanými daty"""
    # extrahování údajů do hlavičky
    hlavicka = ["kód obce", "název obce", "voliči v seznamu", "vydané obálky", "platné hlasy"]
    req_hlavicka = requests.get(get_odkazy_obci(url)[0])
    soup_hlavicka = bs(req_hlavicka.text, "html.parser")
    for prvek in soup_hlavicka.find_all("td", {"headers": ["t1sb2", "t2sb2"]}):
        nadpis = prvek.text
        hlavicka.append(nadpis)
    nalezene_udaje, spojene_udaje = [], []
    # připojení hlavičky
    spojene_udaje.append(hlavicka)
    # extrahování a připojení dat z jednotlivých odkazů k daným obcím
    index = 0
    for link in get_odkazy_obci(url):
        req_detaily = requests.get(link)
        soup_detaily = bs(req_detaily.text, "html.parser")
        nalezene_udaje.append(get_cisla_obci(url)[index])
        nalezene_udaje.append(get_nazvy_obci(url)[index])
        index += 1
        for elem in soup_detaily.find_all("td", {"headers": ["sa2", "sa3", "sa6", "t1sb3", "t2sb3"]}):
            text = elem.text
            nalezene_udaje.append(text)
        spojene_udaje.append(nalezene_udaje)
        nalezene_udaje = []
    return spojene_udaje


def save_as_csv(data, filename) -> None:
    """Funkce prochází list listů a zapisuje do csv souboru"""
    f = open(filename, "w", encoding="utf-8", newline="")
    f_writer = csv.writer(f)
    for podlist in data:
        f_writer.writerow(podlist)
    f.close()


if __name__ == "__main__":
    main()
