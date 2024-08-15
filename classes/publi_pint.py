import os
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from PIL import Image


class PublishInPinterest():
    def __init__(self, driver):
        # Open the desired webpage
        self.driver = driver
        self.driver.get('https://www.pinterest.com/')

    def login(self, login_email, login_pass):
        # Wait for the element to be present (optional, but recommended for dynamic content)
        self.driver.implicitly_wait(10)

        # Locate the button by its unique data-test-id attribute
        button = self.driver.find_element(By.CSS_SELECTOR, '[data-test-id="simple-login-button"] button')

        # Click the button
        button.click()

        # Wait for the email input field to be present
        self.driver.implicitly_wait(10)

        # Locate the input field by its id and send the email
        email_input = self.driver.find_element(By.ID, 'email')
        email_input.send_keys(login_email)
        
        self.driver.implicitly_wait(10)

        # Pause for 1
        sleep(1)

        # Locate the input field by its id and send the email
        email_input = self.driver.find_element(By.ID, 'password')
        email_input.send_keys(login_pass)

        # Locate the submit button by its data-test-id attribute
        submit_button = self.driver.find_element(By.CSS_SELECTOR, '[data-test-id="registerFormSubmitButton"] button')

        # Click the submit button
        submit_button.click()

        # Pause for 5
        sleep(5)

    def pulish_image(self, image_path, link, title, collection=None, description=''):
        # Define the target size for the image
        min_width, min_height = 200, 300
        target_size = (min_width, min_height)

        try:
            # Check image size
            with Image.open(image_path) as img:
                width, height = img.size

            # Rescale if the image is smaller than the minimum size
            if width < min_width or height < min_height:
                print(f"Image {image_path} is {width}x{height}. Rescaling...")
                self.rescale_images(image_path, target_size)
        except Exception as e:
            print(f"Error checking image size ({image_path}): {e}")

        try:
            # Locate the "Crear Pin" div by its data-test-id attribute
            self.driver.get('https://www.pinterest.com/business/hub/')

            sleep(1)
            create_pin_div = self.driver.find_element(By.CSS_SELECTOR, '[data-test-id="onboarding-module-create-pin-button"]')
            # Click the "Crear Pin" div
            create_pin_div.click()

            # Pause for 5
            sleep(2)

            # Locate the file input element by its data-test-id attribute
            file_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test-id^="media-upload-input"]'))
            )
            # Send the file path to the file input element
            absolute_path = os.path.abspath(image_path)
            file_input.send_keys(absolute_path)

            sleep(2)


            # Locate the textarea by placeholder text
            textarea = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//textarea[@placeholder="Agrega un título"]'))
            )
            # Send keys to the textarea
            textarea.send_keys(title[:60])

            sleep(2)

            # Locate the contenteditable div by its ID or other attributes
            contenteditable_div = self.driver.find_element(By.CSS_SELECTOR, 'div[contenteditable="true"]')
            # Click on the contenteditable div to focus it
            contenteditable_div.click()
            # Clear any existing text (optional, if necessary)
            contenteditable_div.send_keys(Keys.CONTROL + "a")
            contenteditable_div.send_keys(Keys.BACKSPACE)
            # Send the text to the contenteditable div
            contenteditable_div.send_keys(description[:500])

            sleep(2)

            textarea2 = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//textarea[@placeholder="Agregar un enlace de destino"]'))
            )        # Send the text to the textarea
            textarea2.send_keys(link)

            # Locate the collection if provided
            if collection:
                collection_btn = self.driver.find_element(By.CSS_SELECTOR, 'button[data-test-id="board-dropdown-select-button"]')
                collection_btn.click()
                collection_select = self.driver.find_element(By.XPATH, f'//div[@title="{collection}"]')
                collection_select.click()

            # Locate the button to publish
            button = self.driver.find_element(By.CSS_SELECTOR, '[data-test-id="board-dropdown-save-button"]')
            button.click()

            # Pause for 15 seconds to observe the result
            random_int = random.randint(12, 25)
            sleep(random_int)
            return True
        except:
            return False

    def close_browser(self):
        # Optional: Close the browser after the action
        self.driver.quit()


    @staticmethod
    def rescale_image(image_path, target_size):
        # Loop through all files in the specified folder
        with Image.open(image_path) as img:
            # Resize the image to the target size
            resized_img = img.resize(target_size, Image.LANCZOS)
            
            # Save the resized image, overwriting the original file
            resized_img.save(image_path)
