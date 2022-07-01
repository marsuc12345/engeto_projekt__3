import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import csv


url = "https://volby.cz/pls/ps2021/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2109"
vystup = "pokus.csv"


# faze 1 z linku vyse skrejpovat LINK, NAZEV a CISLO obci do listu

req_obce = requests.get(url)
soup_obce = bs(req_obce.text, "html.parser")

nalezene_odkazy = []
for a_elem in soup_obce.find_all("a"):
    href = urljoin(url, a_elem["href"])
    if len(href) > 70 and href not in nalezene_odkazy:
        nalezene_odkazy.append(href)

nalezene_obce = []
for elem in soup_obce.find_all("td",{"class":"overflow_name"}):
    text = elem.text
    nalezene_obce.append(text)

nalezene_cisla = []
for elem in soup_obce.find_all("td",{"headers":["t1sb1","t2sb1","t3sb1"]}):
    text = elem.text
    nalezene_cisla.append(text)


# faze 2 skrejpovat HLAVICKU a potrebne NALEZENE udaje a ulozit vse do .CSV

hlavicka = ["kód obce","název obce","voliči v seznamu","vydané obálky","platné hlasy"]
req_hlavicka = requests.get(nalezene_odkazy[0])
soup_hlavicka = bs(req_hlavicka.text, "html.parser")
for prvek in soup_hlavicka.find_all("td", {"headers": ["t1sb2","t2sb2"]}):
    nadpis = prvek.text
    hlavicka.append(nadpis)
print(hlavicka)
f = open(vystup, "w", encoding="utf-8", newline="")
f_writer = csv.writer(f)
f_writer.writerow(hlavicka)

nalezene_udaje = []
index = 0
for link in nalezene_odkazy:
    req_detaily = requests.get(link)
    soup_detaily = bs(req_detaily.text, "html.parser")
    nalezene_udaje.append(nalezene_cisla[index])
    nalezene_udaje.append(nalezene_obce[index])
    index += 1
    for elem in soup_detaily.find_all("td",{"headers":["sa2","sa3","sa6","t1sb3","t2sb3"]}):
        text = elem.text
        nalezene_udaje.append(text)
    f_writer.writerow(nalezene_udaje)
    print(nalezene_udaje)
    nalezene_udaje = []
f.close()
