import os
import json
import requests
import pyperclip
import uuid
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class ScrapeCJProducts():
    def __init__(self, driver):
        # Open the desired webpage
        self.driver = driver
        self.driver.get('https://signin.cj.com/u/login/')

    def login(self, login_email, login_pass):
        # Wait for the element to be present (optional, but recommended for dynamic content)
        self.driver.implicitly_wait(10)

        # Wait for the email input field to be present
        self.driver.implicitly_wait(10)

        # Locate the input field by its id and send the email
        email_input = self.driver.find_element(By.ID, 'username')
        email_input.send_keys(login_email)
        
        self.driver.implicitly_wait(10)

        # Locate the button using its name attribute and click it
        button = self.driver.find_element(By.NAME, "action")
        button.click()

        # Pause for 1
        sleep(1)

        # Locate the input field by its id and send the email
        email_input = self.driver.find_element(By.ID, 'password')
        email_input.send_keys(login_pass)

        # Locate the button using its name attribute and click it
        button = self.driver.find_element(By.NAME, "action")
        button.click()

        # Pause for 5
        sleep(5)


    def get_products_by_advertiser(self):
        hrefs = {'Flowers': ['https://members.cj.com/member/6774140/publisher/links/search/#!tab=products&advertiserIds=857900'], 'Computer SW': ['https://members.cj.com/member/6774140/publisher/links/search/#!tab=products&advertiserIds=6260179', 'https://members.cj.com/member/6774140/publisher/links/search/#!tab=products&advertiserIds=998086'], 'Virtual Malls': ['https://members.cj.com/member/6774140/publisher/links/search/#!tab=products&advertiserIds=4498040'], 'Toys': ['https://members.cj.com/member/6774140/publisher/links/search/#!tab=products&advertiserIds=2357926'], 'Gifts': ['https://members.cj.com/member/6774140/publisher/links/search/#!tab=products&advertiserIds=4046728'], 'Electronic Games': ['https://members.cj.com/member/6774140/publisher/links/search/#!tab=products&advertiserIds=4518745'], 'Jewelry': ['https://members.cj.com/member/6774140/publisher/links/search/#!tab=products&advertiserIds=4295086']}  # Initialize an empty dictionary to store category-href pairs

        if not hrefs:
            self.driver.implicitly_wait(20)
            toggle_partners = self.driver.find_element(By.ID, "pub-partners")
            toggle_partners.click()

            # Locate the <a> element by its ID and click it
            a_element = self.driver.find_element(By.ID, "pub-partners-advertisers-myAdvertisers")
            a_element.click()

            self.driver.implicitly_wait(15)

            # Locate all product row wrappers
            product_rows = self.driver.find_elements(By.CLASS_NAME, "adv-row-wrapper")

            for row in product_rows:
                # Extract category name
                try:
                    category_div = row.find_element(By.CLASS_NAME, "category-name")
                    category_name = category_div.text.strip()
                except:
                    # Handle cases where the category name is not present
                    category_name = "Unknown"

                # Check if the 'get-products-container' div is present within the row
                try:
                    nested_div_lvl0 = row.find_element(By.CLASS_NAME, "adv-row")
                    nested_div_lvl1 = nested_div_lvl0.find_element(By.CLASS_NAME, "main-row-wrapper")
                    nested_div_lvl2 = nested_div_lvl1.find_element(By.CLASS_NAME, "buttons adv-row-vertical-sep")
                    get_products_container = nested_div_lvl2.find_element(By.CLASS_NAME, "get-products-container")

                    # Find all <a> tags within the get-products-container
                    a_tags = get_products_container.find_elements(By.TAG_NAME, "a")
                except:
                    # If not present, find <a> tags within the row directly
                    print("no get-products-container")
                    a_tags = row.find_elements(By.TAG_NAME, "a")

                # Extract href attributes and store them in the dictionary
                for a in a_tags:
                    href = a.get_attribute("href")
                    if href:
                        if category_name not in hrefs:
                            hrefs[category_name] = []
                        hrefs[category_name].append(href)

        # Print the dictionary of hrefs
        print(hrefs)
        return hrefs

    def get_products(self, link, category):
        self.driver.get(link)
        # Reload the page
        self.driver.refresh() 
        self.driver.implicitly_wait(15)
        file_path = os.path.join('cjproducts', 'data_dictionary.json')
        i=0

        # Open and load the JSON content from the file
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Locate all product row wrappers
        product_rows = self.driver.find_elements(By.CLASS_NAME, "product-row-wrapper")

        for row in product_rows:
            i+=1
            name, description, price = None, None, None

            # Locate the div with the class 'fl link-preview' within the current row
            link_preview_divs = row.find_elements(By.CLASS_NAME, "fl.link-preview")
            
            if link_preview_divs:
                # Click on the first 'fl link-preview' div in the current row
                link_preview_divs[0].click()

            # Locate all 'detail' divs within the row
            detail_divs = row.find_elements(By.CLASS_NAME, "detail")
            
            for detail in detail_divs:
                # Get the label text
                label = detail.find_element(By.CLASS_NAME, "detail-label").text.strip()
                #print('label: ', label)
                # Get the corresponding value text
                value = detail.find_element(By.CLASS_NAME, "value").text.strip()
                if label == "Name":
                    name = value
                elif label == "Description":
                    description = value
                elif label == "Price":
                    price = value

                #print(name)
                if name and description and price:
                    data[name] = {'description': description, 'price': price}
                    break

            try:
                if data[name]["image"] != None:
                    print('Image already in memory', data[name]["image"])
            except KeyError as e:
                    # Click the "get code" to get link and download image
                    # Locate the <li> element of the "get code"
                    li_element = row.find_element(By.CSS_SELECTOR, 'li[data-nav-id="getCode"]')
                    # Locate the <a> element inside this <li> and click
                    a_element = li_element.find_element(By.TAG_NAME, "a")
                    a_element.click()


                    url_element = row.find_element(By.ID, "clickUrlLabel")
                    # Locate the <a> element that provides the ref link
                    clickurl_element = url_element.find_element(By.TAG_NAME, "a")
                    # Click the <a> element
                    clickurl_element.click()

                    url_click_tab = row.find_element(By.ID, "clickUrlTab")
                    # Locate and interact with the element containing the desired text
                    textarea = WebDriverWait(url_click_tab, 20).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "clickUrlCode"))
                    )
                    # Focus on the textarea
                    textarea.click()
                    sleep(1)
                    # Select all content and copy it
                    textarea.send_keys(Keys.CONTROL + 'a')  # Select all
                    textarea.send_keys(Keys.CONTROL + 'c')  # Copy to clipboard
                    # Wait a short time to ensure clipboard operation completes
                    sleep(1)
                    # Retrieve content from the clipboard
                    text_content = pyperclip.paste()
                    print('\nlink: ', text_content)
                    data[name]['link'] = text_content
                    sleep(2)
                    
                    link_image_element = row.find_element(By.ID, "imageUrlLabel")
                    click_link_element = link_image_element.find_element(By.TAG_NAME, "a")
                    # Click the <a> element
                    click_link_element.click()

                    image_click_tab = row.find_element(By.ID, "imageUrlTab")
                    link_text_tarea = WebDriverWait(image_click_tab, 20).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "imageUrlCode"))
                    )
                    link_text_tarea.click()
                    sleep(1)
                    # Select all content and copy it
                    link_text_tarea.send_keys(Keys.CONTROL + 'a')  # Select all
                    link_text_tarea.send_keys(Keys.CONTROL + 'c')  
                    # Wait a short time to ensure clipboard operation completes
                    sleep(1)
                    # Retrieve the URL from the 'textarea'
                    image_url = pyperclip.paste()
                    print('iamge url: ', image_url)
                    sleep(2)
                    print(f'\rcount --> {i}:', end='', flush=True)

                    #print('Image URL: ', image_url, end='', flush=True)
                    # Download the image
                    image_name = self.download_image(image_url)

                    data[name]["image"] = image_name

            data[name]["category"] = category

            # Locate the div with the class 'fl link-preview' within the current row
            link_preview_divs_close = row.find_elements(By.CLASS_NAME, "fl.link-preview")
            if link_preview_divs_close:
                # Click on the first 'fl link-preview' div in the current row
                link_preview_divs_close[0].click()
            #print(data)

        with open(file_path, 'w') as file:
            json.dump(data, file, indent=2)
        



    @staticmethod
    def download_image(image_url, save_folder='cjproducts'):
        # Ensure the save folder exists
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        # Extract the image filename from the URL
        if image_url.endswith(('.png', '.jpg', '.jpeg')):
            image_filename = str(uuid.uuid4())
            image_filename += ('.' + image_url.split('.')[-1])
        else:
            print('rare ending')
            image_filename = str(uuid.uuid4())
            image_filename += '.png'
        file_path = os.path.join(save_folder, image_filename)

        try:
            # Send a GET request to fetch the image
            response = requests.get(image_url, stream=True)
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Write the image content to a file
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)

            print(f"Image successfully downloaded and saved to {file_path}", end='', flush=True)
            return image_filename

        except requests.RequestException as e:
            print(f"An error occurred: {e}")