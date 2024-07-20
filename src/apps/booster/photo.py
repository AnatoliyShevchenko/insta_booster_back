# Third-Party
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# Python
import time

# Local
from .base import BaseForBooster


class ActionsWithPhoto(BaseForBooster):
    """Class for actions with photo."""

    @staticmethod
    def write_comment(driver: WebDriver) -> bool:
        try:
            comment = WebDriverWait(driver, 10).until(
                ec.presence_of_element_located((
                    By.XPATH, '//*[contains(@id, "mount_")]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/div[2]/div/div[4]/section/div/form/div/textarea'
                ))
            )
            time.sleep(5)
            comment.send_keys("nice")
            time.sleep(5)
            print("Comment added")
            return True
        except Exception as e:
            return False

    @staticmethod
    def send_comment(driver: WebDriver) -> bool:
        try:
            button = WebDriverWait(driver, 10).until(
                ec.presence_of_element_located((
                    By.XPATH, '//*[contains(@id, "mount_")]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/div[2]/div/div[4]/section/div/form/div/div[2]/div'
                ))
            )
            button.click()
            time.sleep(5)
            print("Comment sent")
            time.sleep(5)
            return True
        except Exception as e:
            return False

    def make_comment(self, driver: WebDriver) -> bool:
        written = self.write_comment(driver=driver)
        if not written:
            return False
        sent = self.send_comment(driver=driver)
        if not sent:
            return False
        return True

    def increase_likes(self, driver: WebDriver) -> bool:
        path = '//*[contains(@id, "mount_")]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/div[2]/div/div[3]/section[1]/div[1]/span[1]/div/div'
        try:
            button = WebDriverWait(driver, 10).until(
                ec.element_to_be_clickable((By.XPATH, path))
            )
            time.sleep(1)
            button.click()
            time.sleep(1)
            button.click()
            return True
        except Exception as e:
            return False
