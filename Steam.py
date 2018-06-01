import requests
from bs4 import BeautifulSoup
from pyzabbix import ZabbixMetric, ZabbixSender
import time

def send_stats_to_zabbix(metric_key, metric_data):
    hostname = "Steam"
    packet = []
    for key in metric_data:
        if key.startswith("Bless Online"):
            zabbix_item = metric_key + '[' + key + ']'
            packet.append(ZabbixMetric(hostname, zabbix_item, rank.index(key) + 1))
            print(zabbix_item)

    result = ZabbixSender(zabbix_server='127.0.0.1', use_config=False).send(packet)
    return result

def get_data(url):
    session = requests.Session()
    session.verify = False

    resp = session.get(url)
    data = resp.content

    return data

def get_rank(data, search_key, search_class):
    soup = BeautifulSoup(data, 'html.parser')
    count = 0
    rank = []

    for itemText in soup.find_all(search_key, attrs={'class': search_class}):
        count = count + 1
        print("%s %s" % (count, itemText.string))
        rank.append(itemText.string)
    return rank

config_data = [{
        'key': 'seller',
        'url': 'https://store.steampowered.com/search/?filter=globaltopsellers&os=win',
        'search-key': 'span',
        'search-class': 'title',
        }, {
        'key': 'player',
        'url': 'https://store.steampowered.com/stats/',
        'search-key': 'a',
        'search-class': 'gameLink',
        }]

while True:
    try:
        for item in config_data:
            data = get_data(item['url'])

            rank = get_rank(data, item['search-key'], item['search-class'])

            send_stats_to_zabbix(item['key'], rank)
            time.sleep(10)
    except Exception as e:
        print("error %s" % e)
        time.sleep(10)
