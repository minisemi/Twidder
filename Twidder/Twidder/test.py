from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest


#IMPORTANT! Change path if account is switched
path = "/home/matso354/TDDD97/lab1/Twidder/chromedriver"


def set_up(self):
    self.driver = webdriver.chromer(path)
    self.driver.get('localhost:5000')
    time.sleep(3)

