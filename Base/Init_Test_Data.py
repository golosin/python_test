import xml.etree.ElementTree as ET


def init_data():
    dict_init_data = {}

    tree = ET.parse('autoTest_InitData.xml')
    root = tree.getroot()

    dict_init_data["environment"] = root.find('environment').text
    dict_init_data["email"] = root.find('login').text
    dict_init_data["password"] = root.find('password').text
    dict_init_data["pipeline"] = root.find('pipeline').text

    testFeed = root.find('testFeed')
    yml_feed = testFeed.find('yml_feed')
    dict_init_data["yml_name_feed"] = yml_feed.get('name_feed')
    dict_init_data["yml_desktop_location"] = yml_feed.find('desktop_location').text
    dict_init_data["yml_url_location"] = yml_feed.find('url_location').text

    google_feed = testFeed.find('google_feed')
    dict_init_data["GF_name_feed"] = google_feed.get('name_feed')
    dict_init_data["GF_desktop_location"] = google_feed.find('desktop_location').text
    dict_init_data["GF_url_location"] = google_feed.find('url_location').text

    csv_feed = testFeed.find('csv_feed')
    dict_init_data["csv_name_feed"] = csv_feed.get('name_feed')
    dict_init_data["csv_desktop_location"] = csv_feed.find('desktop_location').text
    dict_init_data["csv_url_location"] = csv_feed.find('url_location').text


    return dict_init_data