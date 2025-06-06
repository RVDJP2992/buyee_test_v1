import requests
from bs4 import BeautifulSoup

def get_ebay_prices(query):
    url = f"https://www.ebay.co.uk/sch/i.html?_nkw={query}"
    res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(res.text, 'html.parser')
    items = soup.select('.s-item')

    results = []
    for item in items[:5]:
        title = item.select_one('.s-item__title')
        price = item.select_one('.s-item__price')
        link = item.select_one('.s-item__link')
        if title and price and link:
            results.append({
                'title': title.get_text(),
                'price': price.get_text(),
                'url': link['href']
            })
    return results

def get_buyee_prices(query):
    url = f"https://buyee.jp/item/search/query/{query}/category/0"
    res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(res.text, 'html.parser')
    items = soup.select('.itemBox')

    results = []
    for item in items[:5]:
        title = item.select_one('.itemTitle')
        price = item.select_one('.price')
        link = item.select_one('a')
        if title and price and link:
            results.append({
                'title': title.get_text(strip=True),
                'price': price.get_text(strip=True).replace('¥','¥ '),
                'url': "https://buyee.jp" + link['href']
            })
    return results

def parse_price(price_str):
    price_str = price_str.replace(',', '').replace('¥', '').replace('£', '')
    try:
        return float(''.join(filter(lambda c: c.isdigit() or c == '.', price_str)))
    except:
        return None

def compare_prices(ebay_data, buyee_data):
    results = []
    for e, b in zip(ebay_data, buyee_data):
        e_price = parse_price(e['price'])
        b_price = parse_price(b['price'])
        if e_price is not None and b_price is not None:
            diff = round(e_price - b_price, 2)
            results.append({
                'ebay': e,
                'buyee': b,
                'difference': diff
            })
    return results