import time
from bs4 import BeautifulSoup
import requests
import base64
from requests_html import HTMLSession



weapons = {
    "AK-47": "weapon_ak47",
    "AWP": "weapon_awp",
    "M4A4": "weapon_m4a1",
    "M4A1-S": "weapon_m4a1_silencer",
    "USP-S": "weapon_usp_silencer",
    "Glock-18": "weapon_glock",
    "Desert Eagle": "weapon_deagle",
    "MP9": "weapon_mp9",
    "MAC-10": "weapon_mac10",
    "P250": "weapon_p250",
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
        'qr_code_verify_ticket': '4afP8V1bc08f05d0a41e76d35ddbbc412dba',
        'remember_me': 'U1103613490|xtutxW1ofFbvLHMzWcTPdZNeVhWajkUn',
        'session': '1-X7g_JYBGT-SVQ3jzmKJZUdScFXdAUPM1n2E4Fx5UKua62030653802',
        'csrf_token': 'Ijc1M2U5YjM0ZDFjZjkwMmI1MmExMzAyYTE0YmYwYzA4NWY3MTczYTki.F7VYGQ.ZR0sIDr7kzxOnunsUvpcRoe3sbY',
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        # 'Cookie': 'Device-Id=G4fFCRE0U92s5dsUF5q8; P_INFO=351-911556587|1685714431|1|netease_buff|00&99|null&null&null#PT&null#10#0|&0||351-911556587; Locale-Supported=en; game=csgo; qr_code_verify_ticket=4afP8V1bc08f05d0a41e76d35ddbbc412dba; remember_me=U1103613490|xtutxW1ofFbvLHMzWcTPdZNeVhWajkUn; session=1-X7g_JYBGT-SVQ3jzmKJZUdScFXdAUPM1n2E4Fx5UKua62030653802; csrf_token=Ijc1M2U5YjM0ZDFjZjkwMmI1MmExMzAyYTE0YmYwYzA4NWY3MTczYTki.F7VYGQ.ZR0sIDr7kzxOnunsUvpcRoe3sbY',
        'Referer': 'https://buff.163.com/market/csgo',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
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
        '_': '1691599786938',
    }

    clientId = "063ed991124a407bb6809f1bb6b637ea"
    clientSecret = "tRyVL1b3v86RJpxctrl+zkx13JXIL6fu6C5Z+sUiwg8K+baIHiWcEeemqUN2Ug2W01Km968Dw5VhGKm0let4ew=="
    clientData = f"{clientId}:{clientSecret}"
    encodedData = str(base64.b64encode(clientData.encode("utf-8")), "utf-8")
    authorizationHeaderString = f"Basic {encodedData}"

    try:
        response = requests.get('https://buff.163.com/api/market/goods', params=params, cookies=cookies,
                                headers=headers)


        for item in response.json()["data"]["items"]:
            print(item["market_hash_name"])
            short_name = item["short_name"]
            buff_price = float(item["sell_min_price"]) * 0.12610534
            condition = item["goods_info"]["info"]["tags"]["exterior"]["localized_name"]
            icon_url = item["goods_info"]["icon_url"]
            skin = Skin(short_name, buff_price, condition)
            skin.icon_url = icon_url

            querySkins.append(skin)

        print("skinport query")
        r = requests.get("https://api.skinport.com/v1/sales/history", headers={
            "authorization": authorizationHeaderString}, params={
            # "market_hash_name": queryString,
            "app_id": 730,
            "currency": "EUR"

        }).json()
        print("skinport query done")
        for item in r:
            print(item["market_hash_name"])
            for skin in querySkins:
                #print(item["market_hash_name"])
                skin_name = skin.name + " (" + skin.condition + ")"
                #print(skin_name)
                if skin_name == item["market_hash_name"]:
                    print(item)
                    month_average = item["last_30_days"]["avg"]
                    skin.skinPortPrice = float(month_average)
                    skin.profit = skin.skinPortPrice * 0.88 - skin.buffPrice
                    skin.profitPercentage = skin.profit / skin.buffPrice * 100
                    #print(f"Name: {skin.name} Condition: {skin.condition} Profit: {skin.profitPercentage} Skinport Price)")

    except (requests.exceptions.RequestException, KeyError, TypeError):
        return []

    return querySkins


