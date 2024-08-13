from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from classes.scrape_cjprods import ScrapeCJProducts
from time import sleep

def main():
    login_email = 'jose.pgilsuarez@gmail.com'
    login_pass = 'Pedrogil071999-'

    # Instanciate the webdriver
    driver = webdriver.Chrome()

    cj_scraper = ScrapeCJProducts(driver)
    cj_scraper.login(login_email, login_pass)
    cj_scraper.get_products_by_advertiser()

if __name__ == "__main__":
    main()
