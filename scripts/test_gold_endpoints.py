import requests
urls = [
    'https://data-asg.goldprice.org/dbXau/USD',
    'https://api.metals.live/v1/spot/gold',
    'https://api.metals.live/v1/spot',
    'https://api.metals.live/v1/spot/xau',
    'https://www.goldapi.io/api/XAU/USD',
    'https://api.metals-api.com/v1/latest?base=XAU&symbols=USD'
]
for url in urls:
    try:
        r = requests.get(url, timeout=5)
        print(url, r.status_code, r.text[:200])
    except Exception as e:
        print(url, 'ERR', e)
