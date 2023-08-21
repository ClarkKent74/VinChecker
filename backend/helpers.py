import time
import logging

from typing import Optional
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class VinParser:
    "Класс для парсинга информации об автомобиле по vin номеру"
    def __init__(self, vin: str):
        self.vin = vin
        self.url = "https://avtocod.ru/"
        self.options = ChromeOptions()
        self.options.add_argument("start-maximized")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-extensions")
        self.options.add_argument('--disable-application-cache')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-setuid-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--headless")

    def parse(self) -> Optional[dict]:
        """
        Получаем словарь со всеми доступными характеристиками автомобиля
        """
        try:
            with Chrome(options=self.options) as driver:
                driver.get(self.url)
                vin_button = driver.find_element(By.XPATH, '//*[@id="check-head"]/div/div[1]/div/label[2]/span/span')
                vin_button.click()

                vin_input = driver.find_element(By.XPATH, '//*[@id="test"]')
                vin_input.click()
                vin_input.send_keys(self.vin)

                vin_check_button = driver.find_element(By.XPATH, '//*[@id="check-head"]/div/div[3]/div/button')
                vin_check_button.click()

                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    '//*[@id="names"]/div/div/div/div[2]/div[2]/div[1]/div/div[2]/h1')))

                model_year = (driver.find_element(By.XPATH,
                                                  '//*[@id="names"]/div/div/div/div[2]/div[2]/div[1]/div/div[2]/h1')). \
                    text.split(', ')
                print(model_year)
                model = model_year[0]
                print(model)
                year = model_year[1].split()[0]
                category = (
                    driver.find_element(By.XPATH, '//*[@id="short-info"]/div/ul[1]/li[2]/div/div/div[2]/span')).text
                print(category)
                wheel_position = (
                    driver.find_element(By.XPATH, '//*[@id="short-info"]/div/ul[1]/li[3]/div/div/div[2]/span')).text
                print(wheel_position)
                type_engine = (
                    driver.find_element(By.XPATH, '//*[@id="short-info"]/div/ul[2]/li[1]/div/div/div[2]/span')).text
                print(type_engine)
                power_engine = (
                    driver.find_element(By.XPATH, '//*[@id="short-info"]/div/ul[2]/li[2]/div/div/div[2]/span')
                    .text.split()[0])
                print(power_engine)
                volume_engine = \
                    (driver.find_element(By.XPATH, '//*[@id="short-info"]/div/ul[2]/li[3]/div/div/div[2]/span')) \
                        .text.split()[0]
                print(volume_engine)
                time.sleep(5)
            return {
                'Model': model,
                'Year': year,
                'Category': category,
                'Wheel position': wheel_position,
                'Type engine': type_engine,
                'Power engine': power_engine,
                'Volume engine': volume_engine
            }

        except Exception as e:
            logging.error("Exception", exc_info=e)
            print(e)
            return None


def ru_to_en(vin: str) -> str:
    """
    Заменяем в vin номере русские буквы на английские.
    """
    ru_alph = ['е', 'н', 'х', 'в', 'а', 'о', 'с', 'м', 'т', 'у', 'р', 'к']
    en_alph = ['e', 'h', 'x', 'b', 'a', 'o', 'c', 'm', 't', 'y', 'p', 'k']
    result = []
    vin = vin.lower()
    for symb in vin:
        if symb in ru_alph:
            index = ru_alph.index(symb)
            result.append(en_alph[index])
        else:
            result.append(symb)

    return ''.join(result)


