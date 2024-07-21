# Third-Party
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Python
import time

# Local
from .base import BaseForBooster
from src.settings.base import logger


class ActionsWithReels(BaseForBooster):
    """Class for actions with video."""

    @staticmethod
    def increase_likes(driver: WebDriver) -> bool:
        path = '//*[contains(@id, "mount_")]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div[1]/span/div/div'
        try:
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, path))
            )
            time.sleep(5)
            button.click()
            time.sleep(1)
            button.click()
            logger.info(msg="Like sent!")
            return True
        except:
            return False
    
    @staticmethod
    def open_comments(driver: WebDriver):
        path = '//*[contains(@id, "mount_")]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div[2]/div'
        try:
            place = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, path))
            )
            time.sleep(5)
            place.click()
            time.sleep(1)
            place.click()
            logger.info(msg="Comments opened!")
            return True
        except:
            return False

    @staticmethod
    def write_comment(driver: WebDriver) -> bool:
        path = '//*[contains(@id, "mount_")]/div/div/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div[1]'
        try:
            comment = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, path))
            )
            time.sleep(5)
            comment.send_keys("nice")
            time.sleep(5)
            logger.info(msg="Comment added!")
            return True
        except:
            return False

    @staticmethod
    def send_comment(driver: WebDriver) -> bool:
        path = '//*[contains(@id, "mount_")]/div/div/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div/div/div/div[1]/div/div[3]/div/div/div/div/div[3]/div/div[1]'
        try:
            button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, path))
            )
            button.click()
            time.sleep(5)
            logger.info(msg="Comment sent!")
            return True
        except:
            return False

    def make_comment(self, driver: WebDriver) -> bool:
        opened = self.open_comments(driver=driver)
        if not opened:
            return False
        written = self.write_comment(driver=driver)
        if not written:
            return False
        sended = self.send_comment(driver=driver)
        if not sended:
            return False
        return True
