import sys
import csv

import bs4
from bs4 import BeautifulSoup
import requests

def ziskani_odkazu(adresa_URL):
    geter = requests.get(adresa_URL)
    soupp = bs4.BeautifulSoup(geter.text, 'html.parser')
    print(f'STAHUJI DATA z adresy: {adresa_URL}')
    return soupp
soup = ziskani_odkazu(sys.argv[1])
def seznam_měst() -> list:
    citys = []
    search_city = soup.find_all('td','overflow_name')
    for city in search_city:
        citys.append(city.text)
    return citys
def adresa_mest() -> list:
    path = []
    search_path = soup.find_all('td','cislo','href')
    for link_city in search_path:
        link_city = link_city.a['href']
        path.append(f'https://volby.cz/pls/ps2017nss/{link_city}')
    return path

def get_id_mesta() -> list:
    id_city = []
    id = soup.find_all('td','cislo')
    for i in id:
        id_city.append(i.text)
    return id_city


def policy_page() -> list:
    page = []
    city = adresa_mest()
    repsonse = requests.get(city[0])
    soup = bs4.BeautifulSoup(repsonse.text,'html.parser')
    party = soup.find_all('td', 'overflow_name')
    for p in party:
        page.append(p.text)
    return page

def info_voter() -> list:
    voter = []
    addres = adresa_mest()
    for link in addres:
        html = requests.get(link)
        soup = bs4.BeautifulSoup(html.text, 'html.parser')
        pepople = soup.find_all('td', headers='sa2')
        for p in pepople:
            #p = p.text
            voter.append(p.text)
    return voter

def info_attend() -> list:
    attend = []
    addres = adresa_mest()
    for link in addres:
        html = requests.get(link)
        soup = bs4.BeautifulSoup(html.text, 'html.parser')
        pepople = soup.find_all('td', headers='sa3')
        for p in pepople:
            #p = p.text
            attend.append(p.text)
    return attend

def info_corect() -> list:
    corect = []
    addres = adresa_mest()
    for link in addres:
        html = requests.get(link)
        soup = bs4.BeautifulSoup(html.text, 'html.parser')
        pepople = soup.find_all('td', headers='sa6')
        for p in pepople:
            #p = p.text
            corect.append(p.text)
    return corect

def party_votes_precent() -> list:
    address = adresa_mest()
    votes = []
    for link in address:
        html = requests.get(link)
        soup = bs4.BeautifulSoup(html.text, 'html.parser')
        votes_page = soup.find_all('td','cislo',headers=["t1sb3",'t2sb3'])
        precent= []
        for p in votes_page:
            precent.append(p.text)
        votes.append(precent)
    return votes

def creator() -> list:
    rows = []
    voter = info_voter()
    attend = info_attend()
    corect = info_corect()
    citys = seznam_měst()
    ids = get_id_mesta()
    votes = party_votes_precent()
    zipped = zip(ids,citys,voter,attend,corect)
    aux_var = []
    for i,t,v,a,c in zipped:
        aux_var.append([i,t,v,a,c])
    zip_all = zip(aux_var,votes)
    for av,vs in zip_all:
        rows.append(av+vs)
    return rows

def play_program(link,file):
    try:
        header = ['Kód obce', 'Název obce', 'Voliči v seznamu', 'Vydané obálky', 'Platné hlasy']
        content = creator()
        parties = policy_page()
        print(f'ukldam da ta do souboru: {file}')
        for party in parties:
            header.append(party)
        with open(file,mode='w', newline='') as f:
            f_writer = csv.writer(f)
            f_writer.writerow(header)
            f_writer.writerows(content)
        print(f'ukoncuje: {sys.argv[0]}')
    except IndexError:
        print("Nastala chyba. Nejspíš máte špatný odkaz nebo jste jej zapomněli dát do uvozovek.")
        quit()



if __name__ == '__main__':
    addressa = sys.argv[1]
    file_name = sys.argv[2]
    play_program(addressa,file_name)