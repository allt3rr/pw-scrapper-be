from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
from scrappers import olx_scrapper

app = FastAPI()

#URL = 'https://www.olx.pl/praca/zawiercie/?search%5Bdist%5D=30&search%5Bfilter_enum_type%5D%5B0%5D=halftime&search%5Bfilter_enum_type%5D%5B1%5D=seasonal&search%5Bfilter_enum_type%5D%5B2%5D=parttime&search%5Bfilter_enum_special_requirements%5D%5B0%5D=student_status&search%5Bfilter_enum_agreement%5D%5B0%5D=zlecenie&search%5Bfilter_enum_agreement%5D%5B1%5D=practice'
URL = 'https://www.olx.pl/praca/zawiercie'

#TODO: maksium obecnie to 52 oferty - lazy loading obejscie

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