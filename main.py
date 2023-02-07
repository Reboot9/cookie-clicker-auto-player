import sys
import time
import keyboard  # For using is_pressed() function to break main cycle

from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchWindowException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chromedriver_path = Path("D:/Development/chromedriver")


class CookieClickerAutoplayer:
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument("window-size=1000,900")
        self.chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(service=Service(executable_path=str(chromedriver_path)),
                                       options=self.chrome_options)
        self.driver.get("https://orteil.dashnet.org/cookieclicker/")
        self.setup()

    def setup(self):
        """Necessary method to choose language and be able to play"""
        try:
            english_lang = EC.presence_of_element_located((By.ID, 'langSelect-EN'))
            WebDriverWait(self.driver, 15).until(english_lang)
            english_lang = self.driver.find_element(By.ID, "langSelect-EN")
            english_lang.click()
            time.sleep(10)
        except TimeoutException:
            print("Timed out loading the page")
            sys.exit()
        except NoSuchWindowException:
            print("User closed the tab")

    def click_on_cookie(self, clicks_amount: int):
        """Method to click on cookie given amount of times"""
        cookie_object = self.driver.find_element(By.ID, "bigCookie")
        for i in range(clicks_amount):
            cookie_object.click()

    def buy_most_expensive_upgrade(self):
        """Method to increase production by buying upgrades(products and upgrades) from in-game store"""
        try:
            store = self.driver.find_elements(By.CLASS_NAME, "enabled")
            for item in store[::-1]:  # To buy most expensive available upgrade
                item.click()
        except:
            pass


def main():
    game = CookieClickerAutoplayer()
    while True:
        try:
            game.click_on_cookie(5)
            if keyboard.is_pressed("q"):  # Quit condition by pressing 'q'
                break
            game.buy_most_expensive_upgrade()
        except NoSuchWindowException:  # Another quit condition when user closes tab
            break


if __name__ == '__main__':
    main()
