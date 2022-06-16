import xml.etree.ElementTree as ET
import datetime


def parsing_data_feed():

    tree = ET.parse('#1_prod.xml')
    root = tree.getroot()

    shop = root.find('shop')
    offers = shop.find('offers')
    offer_data = []
    offer_param = []
    for offer in offers.findall('offer'):
        offer_data.append(offer.get('id'))
        offer_data.append(offer.find('price').text)
        offer_data.append(offer.find('oldprice').text)
        offer_data.append(offer.find('name').text)
        offer_data.append(offer.find('vendor').text)
        offer_data.append(offer.find('count').text)

        for param in offer.findall('param'):
            dict_atr = [param.attrib]
            offer_param.append([dict_atr[0]['name'], param.text])

    return [offer_data, offer_param]


if __name__ == '__main__':
    dict1 = parsing_data_feed()
    print(dict1)
    print()

    print(dict1[0][5])
