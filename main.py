from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()

URL = 'https://www.olx.pl/praca/zawiercie/?search%5Bdist%5D=30&search%5Bfilter_enum_type%5D%5B0%5D=halftime&search%5Bfilter_enum_type%5D%5B1%5D=seasonal&search%5Bfilter_enum_type%5D%5B2%5D=parttime&search%5Bfilter_enum_special_requirements%5D%5B0%5D=student_status&search%5Bfilter_enum_agreement%5D%5B0%5D=zlecenie&search%5Bfilter_enum_agreement%5D%5B1%5D=practice'

@app.get('/')
def root():
    return {"message": "API is running!"}

@app.get('/data')
def get_data(olx: bool):
    resp = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(resp.text, 'html.parser')

    if olx:
        return olx_scrapper(soup)

    return {"message": 'Brak wybranego dostawcy!'}

    


def olx_scrapper(soup):
    offers = []

    cards = soup.select('.jobs-ad-card')
    for i, card in enumerate(cards):
        name_tag = card.select_one('h4')
        name = name_tag.get_text()

        salary_tag = card.find('p', string=lambda s: 'zł' in s)
        salary = salary_tag.get_text() if salary_tag else None

        link_tag = card.find('a', href=lambda s: s and '/oferta/praca/' in s)
        link = link_tag['href'] if link_tag else None

        offers.append({
            "id": i,
            "name": name,
            "salary": salary,
            "link": link
        })

    return {"title": "OLX oferty pracy", "offers": offers}