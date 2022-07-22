import time
import xml.etree.ElementTree as ET
# from Base_functions import get_WB_stock_price_discount



def parsing_data_feed():

    tree = ET.parse('#1_prod.xml')
    # tree = ET.parse('Aliexpress.xml')
    root = tree.getroot()

    shop = root.find('shop')
    offers = shop.find('offers')
    offer_data = []
    offer_param = []
    i = 0
    j = 0
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

def my_def():
    tree = ET.parse('Sbermegamarket(1).xml')
    root = tree.getroot()

    shop = root.find('shop')
    offers = shop.find('offers')
    offer_data = []
    count = -1
    for offer in offers.findall('offer'):
        count = count + 1
        offer_data.append(offer.get('id'))

    # bar = IncrementalBar('Countdown', max=count)

    i = 0
    j = 0
    count_id = 0
    repeat_id = []
    while i <= count:
        j = i + 1
        while j <= count:
            if offer_data[i] == offer_data[j]:
                count_id = count_id + 1
                repeat_id.append(offer_data[j])
                break
            j = j + 1
        i = i + 1
        # bar.next()
    # bar.finish()

    print(repeat_id)
    return [count+1, count_id]


if __name__ == '__main__':
    # test = my_def()
    # print(test)
    # print()

    # dict1 = parsing_data_feed()
    # print(dict1)
    # print()
    # print(dict1[0][1])

    # get_WB_stock_price_discount(100591961)
    print()
    # get_WB_stock_price_discount(100305944)
    print()
    # get_WB_stock_price_discount(100165832)
    # print()
    # get_WB_stock_price_discount(66854865)
    #
    # get_WB_stock_price_discount(140214536)

    # get_WB_stock_price_discount(100591961)

