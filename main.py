import os
import json
import sys
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from classes.scrape_cjprods import ScrapeCJProducts
from classes.publi_pint import PublishInPinterest
from time import sleep

load_dotenv()

def main():
    login_email = os.getenv('LOGIN_EMAIL')
    login_pass = os.getenv('LOGIN_PASS')

    # Instanciate the webdriver
    driver = webdriver.Chrome()

    try:
        if sys.argv[1] == '-d':
            cj_scraper = ScrapeCJProducts(driver)
            cj_scraper.login(login_email, login_pass)
            links_by_advertiser: dict[str, list[str]] = cj_scraper.get_products_by_advertiser()

            print(links_by_advertiser)
            for adv_catego, adv_link in links_by_advertiser.items():
                for link in adv_link:
                    print(f"\nScrapeing into the next advertiser products... {link}\n")
                    cj_scraper.get_products(link, adv_catego)
    except IndexError:
        pass


    file_path = os.path.join('cjproducts', 'data_dictionary.json')

    # Open and load the JSON content from the file
    with open(file_path, 'r') as file:
        data_dict = json.load(file)


    kping_dict = {key: value for key, value in data_dict.items() if (value["category"] == "Toys" or value["category"] == "Electronic Games")}
    print('lenght kping_dict: ', len(kping_dict))
    kping_pint = PublishInPinterest(driver)
    kping_pint.login(os.getenv('LOGIN_EMAIL_PINTKP'), os.getenv('LOGIN_PASS_PINTKP'))
    i = 0
    for key in kping_dict.keys():
        i += 1
        print(f'{i} out of {len(kping_dict)}', end='', flush=True)
        if kping_dict[key]['image'] is not None:       
            image_path = os.path.join('cjproducts', kping_dict[key]['image'])
            affiliate_link = kping_dict[key]['link']
            title = key
            description = kping_dict[key]['description']
            kping_pint.pulish_image(image_path=image_path, link=affiliate_link, title=title, description=description)

    kping_pint.close_browser()

    # Instanciate the webdriver
    driver = webdriver.Chrome()

    soft_dict = {key: value for key, value in data_dict.items() if (value["category"] == "Computer SW" or value["category"] == "Virtual Malls")}
    print('lenght soft_dict: ', len(soft_dict))
    jotalsoft_pint = PublishInPinterest(driver)
    jotalsoft_pint.login(os.getenv('LOGIN_EMAIL_PINTJS'), os.getenv('LOGIN_PASS_PINTJS'))
    i = 0
    for key in soft_dict.keys():
        i += 1
        print(f'{i} out of {len(soft_dict)}', end='', flush=True)
        if soft_dict[key]['image'] is not None:       
            image_path = os.path.join('cjproducts', soft_dict[key]['image'])
            affiliate_link = soft_dict[key]['link']
            title = key
            description = soft_dict[key]['description']
            jotalsoft_pint.pulish_image(image_path=image_path, link=affiliate_link, title=title, description=description)

    jotalsoft_pint.close_browser()

    # Instanciate the webdriver
    driver = webdriver.Chrome()

    flowers_dict = {key: value for key, value in data_dict.items() if (value["category"] == "Flowers" or value["category"] == "Gifts" or value["category"] == "Jewelry")}
    print('lenght flowers_dict: ', len(flowers_dict))
    flowerpower_pint = PublishInPinterest(driver)
    flowerpower_pint.login(os.getenv('LOGIN_EMAIL_PINTFP'), os.getenv('LOGIN_PASS_PINTFP'))
    i = 0
    for key in flowers_dict.keys():
        i += 1
        print(f'{i} out of {len(flowers_dict)}', end='', flush=True)
        if flowers_dict[key]['image'] is not None:
            image_path = os.path.join('cjproducts', flowers_dict[key]['image'])
            affiliate_link = flowers_dict[key]['link']
            title = key
            description = flowers_dict[key]['description']
            flowerpower_pint.pulish_image(image_path=image_path, link=affiliate_link, title=title, description=description)

    flowerpower_pint.close_browser()


if __name__ == "__main__":
    main()
