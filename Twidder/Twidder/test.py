from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest


#IMPORTANT! Change path if account is switched
path = "/home/matso354/TDDD97/lab1/Twidder/chromedriver"

class test_suite (unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(path)
        self.driver.get('localhost:5000')
        time.sleep(3)


    def test_log_in(self):
        driver = self.driver
        email = driver.find_element_by_xpath('//*[@id="loginemail"]')
        pw = driver.find_element_by_xpath('//*[@id="loginpassword"]')
        login_button = driver.find_element_by_xpath('//*[@id="loginButton"]')
        email.send_keys('wrong@email')
        pw.send_keys('wrongpw')
        login_button.click()
        time.sleep(3)
        assert "Sign in failed" in driver.find_element_by_xpath('//*[@id="error"]').text
        email.clear()
        pw.clear()
        self.log_in_help(driver)
        assert 'matilda@gmail.com' in driver.find_element_by_xpath('//*[@id="useremail"]').text
        time.sleep(3)

    def test_post_on_profile(self):
        driver = self.driver
        self.log_in_help(driver)
        textArea = driver.find_element_by_xpath('//*[@id="message"]')
        message = "Hi this is me"
        textArea.send_keys(message)
        post_button = driver.find_element_by_xpath('//*[@id="Home"]/div/div[3]/div/div/button[1]')
        post_button.click()
        time.sleep(3)
        assert message in driver.find_element_by_xpath('//*[@id="' + message + '"]/textarea').text
        refresh_button = driver.find_element_by_xpath('//*[@id="Home"]/div/div[3]/div/div/button[2]')
        refresh_button.click()

    #def test_post_to_others(self):

    #def test_sign_up(self):


    #def test_change_password(self):


    def log_in_help(self, driver):
        email = driver.find_element_by_xpath('//*[@id="loginemail"]')
        pw = driver.find_element_by_xpath('//*[@id="loginpassword"]')
        login_button = driver.find_element_by_xpath('//*[@id="loginButton"]')
        email.send_keys('matilda@gmail.com')
        pw.send_keys('aaaaa')
        login_button.click()
        time.sleep(3)

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()