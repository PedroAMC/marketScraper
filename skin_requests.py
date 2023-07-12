import time
from bs4 import BeautifulSoup
import requests
import base64
from requests_html import HTMLSession
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



weapons = {
    "AK-47": "weapon_ak47",
    "AWP": "weapon_awp",
    "M4A4": "weapon_m4a1",
    "M4A1-S": "weapon_m4a1_silencer",
    "USP-S": "weapon_usp_silencer",
    "Glock-18": "weapon_glock",
    "Desert Eagle": "weapon_deagle",
    "Knife": "knife",
    "Gloves": "hands"
}

conditions = {
    "Factory New": "wearcategory0",
    "Minimal Wear": "wearcategory1",
    "Field-Tested": "wearcategory2",
    "Well-Worn": "wearcategory3",
    "Battle-Scarred": "wearcategory4"
}

class Skin:
    def __init__(self, name, buffPrice, condition):
        self.name = name
        self.buffPrice = buffPrice
        self.condition = condition
        self.skinPortPrice = 0
        self.profit = 0
        self.profitPercentage = 0
        self.iconUrl = "";


def get_skins_bs4(weapon_name, condition, min_price, max_price):
    querySkins = []
    weapon_name = weapons[weapon_name]
    condition = conditions[condition]

    print("running bs4")


    cookies = {
        'Device-Id': 'G4fFCRE0U92s5dsUF5q8',
        'P_INFO': '351-911556587|1685714431|1|netease_buff|00&99|null&null&null#PT&null#10#0|&0||351-911556587',
        'Locale-Supported': 'en',
        'game': 'csgo',
        'qr_code_verify_ticket': 'be5CAuY0913e9edc4805ae380dd8c47af988',
        'remember_me': 'U1103613490|IvTgODLkmEeZwFChbCzshRUTf8wTU6Qp',
        'session': '1-kzDt6A7o9YjXYQk3MWcCIoZkc_jAOgjZZf8fJUnnYDdN2030653802',
        'csrf_token': 'IjlhOWQxZTQ0M2IzNmUzYWMzNzU0YWFiMTEwOGIzMTQ3ZjIxNTE2ZjEi.F4-sww.1Jon4R57YrBQO-dQvndDx70lNtc',
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        # 'Cookie': 'Device-Id=G4fFCRE0U92s5dsUF5q8; P_INFO=351-911556587|1685714431|1|netease_buff|00&99|null&null&null#PT&null#10#0|&0||351-911556587; Locale-Supported=en; game=csgo; qr_code_verify_ticket=be5CAuY0913e9edc4805ae380dd8c47af988; remember_me=U1103613490|IvTgODLkmEeZwFChbCzshRUTf8wTU6Qp; session=1-kzDt6A7o9YjXYQk3MWcCIoZkc_jAOgjZZf8fJUnnYDdN2030653802; csrf_token=IjlhOWQxZTQ0M2IzNmUzYWMzNzU0YWFiMTEwOGIzMTQ3ZjIxNTE2ZjEi.F4-sww.1Jon4R57YrBQO-dQvndDx70lNtc',
        'Referer': 'https://buff.163.com/market/csgo',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
    }

    params = {
        'game': 'csgo',
        'page_num': '1',
        'category': weapon_name,
        'min_price': min_price,
        'max_price': max_price,
        'exterior': condition,
        'use_suggestion': '0',
        '_': '1689131300601',
    }

    clientId = "063ed991124a407bb6809f1bb6b637ea"
    clientSecret = "tRyVL1b3v86RJpxctrl+zkx13JXIL6fu6C5Z+sUiwg8K+baIHiWcEeemqUN2Ug2W01Km968Dw5VhGKm0let4ew=="
    clientData = f"{clientId}:{clientSecret}"
    encodedData = str(base64.b64encode(clientData.encode("utf-8")), "utf-8")
    authorizationHeaderString = f"Basic {encodedData}"

    response = requests.get('https://buff.163.com/api/market/goods', params=params, cookies=cookies, headers=headers)

    queryString = ""
    #print(response.json())
    for item in response.json()["data"]["items"]:
        short_name = item["short_name"]
        buff_price = float(item["sell_min_price"])*0.12610534
        condition = item["goods_info"]["info"]["tags"]["exterior"]["localized_name"]
        icon_url = item["goods_info"]["icon_url"]
        queryString += f"{short_name} ({condition}),"
        skin = Skin(short_name, buff_price, condition)
        skin.icon_url = icon_url

        querySkins.append(skin)


    queryString = queryString[:-1]
    #print(queryString)

    r = requests.get("https://api.skinport.com/v1/sales/history", headers={
    "authorization": authorizationHeaderString}, params={
            #"market_hash_name": queryString,
            "app_id": 730,
            "currency": "EUR"

        }).json()

    for item in r:
        for skin in querySkins:
            skin_name = skin.name + " (" + skin.condition + ")"
            if skin_name == item["market_hash_name"]:
                #print(item)
                month_average = item["last_30_days"]["avg"]
                skin.skinPortPrice = float(month_average)
                skin.profit = skin.skinPortPrice*0.88 - skin.buffPrice
                skin.profitPercentage = skin.profit/skin.buffPrice*100
                #print(f"Name: {skin.name} Condition: {skin.condition} Buff Price: {skin.buffPrice} Skinport Price: {month_average} Profit: {skin.profit}€ Percentage: {skin.profitPercentage}%")
    return querySkins


