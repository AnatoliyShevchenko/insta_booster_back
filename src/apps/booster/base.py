# Third-Party
from stem import Signal
from stem.control import Controller
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Python
import time
from abc import abstractmethod
from typing import Union, Literal

# Local
from src.settings.const import TOR_PASSWORD


class BaseForBooster:
    """Base class for connect with instagram."""

    def __init__(self, username: str, password: str) -> None:
        self.TOR_PASSWORD = TOR_PASSWORD
        self.LOGIN = username
        self.PASSWORD = username

    def renew_connection(self):
        with Controller.from_port(port=9051) as controller:
            controller.authenticate(password=self.TOR_PASSWORD)
            controller.signal(Signal.NEWNYM)

    @staticmethod
    def create_driver() -> WebDriver:
        proxy = "127.0.0.1:9050"
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument(f"--proxy-server=socks5://{proxy}")
        options.add_argument("--disable-dev-shm-usage")
        driver_path = ChromeDriverManager().install()
        service = Service(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    
    def login_instagram(self):
        self.renew_connection()
        driver: WebDriver = self.create_driver()
        driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(5)
        try:
            self.accept_cookies(driver=driver)
            time.sleep(5)
        except Exception as e:
            pass
        try:
            self.auth(driver=driver)
        except Exception as e:
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
        time.sleep(10)
        print("LOGIN SUCCESS")

    @staticmethod
    def accept_cookies(driver: WebDriver):
        path = "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[1]"
        accept = driver.find_element(by=By.XPATH, value=path)
        accept.click()

    @abstractmethod
    def increase_likes(self, driver: WebDriver):
        pass

    @abstractmethod
    def make_comment(self, driver: WebDriver):
        pass

    def get_action(
        self, driver: WebDriver, post_or_reel: str,
        action: Union[Literal["Like"], Literal["Comment"]]
    ):
        ready = False
        temp = False
        while not ready:
            time.sleep(5)
            driver.get(post_or_reel)
            if action == "Like":
                temp = self.increase_likes(driver=driver)
            elif action == "Comment":
                temp = self.make_comment(driver=driver)

            if temp:
                ready = True
