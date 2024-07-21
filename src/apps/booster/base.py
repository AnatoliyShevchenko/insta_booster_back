# Third-Party
from stem import Signal
from stem.control import Controller
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as ec

# Python
import time
from abc import abstractmethod
from typing import Literal

# Local
from src.settings.const import TOR_PASSWORD
from src.settings.base import logger


class BaseForBooster:
    """Base class for connect with instagram."""

    def __init__(self, username: str, password: str) -> None:
        self.TOR_PASSWORD = TOR_PASSWORD
        self.LOGIN = username
        self.PASSWORD = password

    def renew_connection(self):
        with Controller.from_port(port=9051) as controller:
            controller.authenticate(password=self.TOR_PASSWORD)
            controller.signal(Signal.NEWNYM)
            logger.info(msg="New Connection Created!")

    @staticmethod
    def create_driver() -> WebDriver:
        proxy = "127.0.0.1:9050"
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Закомментировать параметр для тестов, чтобы видеть сам браузер
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument(f"--proxy-server=socks5://{proxy}")
        options.add_argument("--disable-dev-shm-usage")
        driver_path = ChromeDriverManager().install()
        service = Service(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        logger.info(msg="Browser has been launched!")
        return driver
    
    def login_instagram(self):
        self.renew_connection()
        driver: WebDriver = self.create_driver()
        driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(30)
        try:
            self.accept_cookies(driver=driver)
            time.sleep(5)
        except Exception as e:
            logger.error(msg="Cookies not accepted:", exc_info=e)
            pass
        try:
            self.auth(driver=driver)
        except Exception as e:
            logger.error(msg="not autorized:", exc_info=e)
            pass
        return driver

    def auth(self, driver: WebDriver):
        username_input = driver.find_element(
            by=By.XPATH, value='//*[@id="loginForm"]/div/div[1]/div/label/input'
        )
        password_input = driver.find_element(
            by=By.XPATH, value='//*[@id="loginForm"]/div/div[2]/div/label/input'
        )
        button = driver.find_element(
            by=By.XPATH, value='//*[@id="loginForm"]/div/div[3]/button/div'
        )
        username_input.send_keys(self.LOGIN)
        password_input.send_keys(self.PASSWORD)
        button.click()
        logger.info(msg="Authentication success!")

    @staticmethod
    def accept_cookies(driver: WebDriver):
        try:
            accept_buttons = WebDriverWait(driver, 10).until(
                ec.presence_of_all_elements_located((
                    By.XPATH, '//button[text()="Разрешить все cookie"]'
                ))
            )
            if accept_buttons:
                accept_buttons[0].click()
                time.sleep(1)
                accept_buttons[0].click()
                logger.info("Cookies accepted!")
            else:
                logger.error(msg="Не найдено ни одного элемента для принятия cookies")
        except Exception as e:
            logger.error(f"Error accepting cookies: {e}")

    @abstractmethod
    def increase_likes(self, driver: WebDriver):
        pass

    @abstractmethod
    def make_comment(self, driver: WebDriver):
        pass

    def get_action(
        self, driver: WebDriver, link: str,
        action: Literal["Likes", "Comments"]
    ):
        ready = False
        temp = False
        while not ready:
            time.sleep(30)
            driver.get(link)
            if action == "Likes":
                temp = self.increase_likes(driver=driver)
            elif action == "Comments":
                temp = self.make_comment(driver=driver)

            if temp:
                ready = True
