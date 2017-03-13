from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



#IMPORTANT! Change path if account is switched
path = "/home/matso354/TDDD97/lab1/Twidder/chromedriver"

class test_suite (unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(path)
        self.driver.get('localhost:7000')

        try:
            WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="currentView"]/div/div[1]/div[1]/div/img'))
            )
        except NoSuchElementException:
            print('Timed out')

    '''
    Test: Log in with wrong email and pw, then correct.
    '''
    def test_log_in(self):
        driver = self.driver
        email = driver.find_element_by_xpath('//*[@id="loginemail"]')
        pw = driver.find_element_by_xpath('//*[@id="loginpassword"]')
        login_button = driver.find_element_by_xpath('//*[@id="loginButton"]')
        email.send_keys('wrong@email')
        pw.send_keys('wrongpw')
        login_button.click()
        try:
            WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="error"]'))
            )
        finally:
            assert "Sign in failed" in driver.find_element_by_xpath('//*[@id="error"]').text
        email.clear()
        pw.clear()
        email_string = "matilda@gmail.com"
        pw_string = "aaaaa"
        self.log_in_help(driver, email_string, pw_string)


    '''
    Test: Post on users own profile.
    '''
    def test_post_on_profile(self):
        driver = self.driver
        email_string = "matilda@gmail.com"
        pw_string = "aaaaa"
        self.log_in_help(driver, email_string, pw_string)
        text_area = driver.find_element_by_xpath('//*[@id="message"]')
        message = "Hi this is me"
        self.post_help(driver, message, text_area, '//*[@id="Home"]/div/div[3]/div/div/button[1]')

    '''
    Test: Search for other user and post on other users profile.
    '''
    def test_post_to_others(self):
        driver = self.driver
        email_string = "matilda@gmail.com"
        pw_string = "aaaaa"
        self.log_in_help(driver, email_string, pw_string)
        browse_button = driver.find_element_by_xpath('//*[@id="browseTab"]')
        browse_button.click()
        try:
            WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="Browse"]/div/div[1]/div/h3'))
            )
        finally:
            assert 'Browse' in driver.page_source

        search_box = driver.find_element_by_xpath('//*[@id="searchEmail"]')
        search_button = driver.find_element_by_xpath('//*[@id="searchButton"]')
        search_box.send_keys('a.ulander@live.se')
        search_button.click()
        try:
            WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="displaySearchEmail"]'))
            )
        finally:
            assert 'a.ulander@live.se' in driver.find_element_by_xpath('//*[@id="displaySearchEmail"]').text
        message = 'hej alex'
        text_area = driver.find_element_by_xpath('//*[@id="searchmessage"]')
        self.post_help(driver, message, text_area, '//*[@id="searchResults"]/div[2]/div/div/button[1]')

    '''
    Test: Sign up, first with blank form, then existing user, then invalid pw.
    '''
    def test_sign_up(self):
        driver = self.driver
        email_string = 'a@a'
        pw_string = 'password'
        first_name = driver.find_element_by_xpath('//*[@id="firstname"]')
        family_name = driver.find_element_by_xpath('//*[@id="familyname"]')
        gender = driver.find_element_by_xpath('//*[@id="gender"]')
        city = driver.find_element_by_xpath('//*[@id="city"]')
        country = driver.find_element_by_xpath('//*[@id="country"]')
        email = driver.find_element_by_xpath('//*[@id="email"]')
        password = driver.find_element_by_xpath('//*[@id="password"]')
        repeat = driver.find_element_by_xpath('//*[@id="repeatpsw"]')
        button = driver.find_element_by_xpath('//*[@id="signupButton"]')
        self.try_blank_form(driver, button)
        form_list = [first_name, family_name, city, country]
        for item in form_list:
            item.send_keys('test')
        password.send_keys(pw_string)
        repeat.send_keys(pw_string)
        self.try_dupe(driver, email, button)
        email.clear()
        email.send_keys(email_string)
        repeat.clear()
        self.try_wrong_password(driver, password, repeat, button, email)
        repeat.clear()
        repeat.send_keys(pw_string)
        button.click()


        self.log_in_help(driver, email_string, pw_string)

    '''
    Test: Try to change password with wrong pw, then invalid new pw, then correct.
    '''
    def test_change_password(self):
        driver = self.driver
        email_string = 'matilda@gmail.com'
        pw_string = 'aaaaa'
        self.log_in_help(driver, email_string, pw_string)
        account_button = driver.find_element_by_xpath('//*[@id="accountTab"]')
        account_button.click()
        try:
            WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="Account"]/div/div[1]/div/h3'))
            )
        finally:
            assert 'Account' in driver.page_source
        old_pw = driver.find_element_by_xpath('//*[@id="changePasswordOld"]')
        new_pw1 = driver.find_element_by_xpath('//*[@id="changePasswordNew1"]')
        new_pw2 = driver.find_element_by_xpath('//*[@id="changePasswordNew2"]')
        #test with wrong password
        old_pw.send_keys('hejejejeh')
        new_pw1.send_keys('newpw')
        new_pw2.send_keys('newpw')
        button = driver.find_element_by_xpath('//*[@id="changePwForm"]/div[4]/div/div/input')
        button.click()
        try:
            WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="passwordText"]')))
        finally:
            assert 'Wrong password' in driver.find_element_by_xpath('//*[@id="passwordText"]').text
        old_pw.clear()
        new_pw2.clear()
        old_pw.send_keys('aaaaa')
        new_pw2.send_keys('different')
        button.click()
        try:
            WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="passwordText"]')))
        finally:
            assert 'Repeat password failed' in driver.find_element_by_xpath('//*[@id="passwordText"]').text

        new_pw2.clear()
        new_pw2.send_keys('newpw')
        button.click()
        try:
            WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="passwordText"]')))
        finally:
            assert 'Successfully changed password' in driver.find_element_by_xpath('//*[@id="passwordText"]').text
        driver.find_element_by_xpath('//*[@id="changePwForm"]/div[4]/div/div/button').click()
        try:
            WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="currentView"]/div/div[1]/div[1]/div/img'))
            )
        except NoSuchElementException:
            print('Timed out')
        self.log_in_help(driver, 'matilda@gmail.com', 'newpw')

        #changing back pw for other tests
        driver.find_element_by_xpath('//*[@id="accountTab"]').click()
        try:
            WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="Account"]/div/div[1]/div/h3'))
            )
        except NoSuchElementException:
            print('Timed out')
        old_pw = driver.find_element_by_xpath('//*[@id="changePasswordOld"]')
        new_pw1 = driver.find_element_by_xpath('//*[@id="changePasswordNew1"]')
        new_pw2 = driver.find_element_by_xpath('//*[@id="changePasswordNew2"]')
        #test with wrong password
        old_pw.send_keys('newpw')
        new_pw1.send_keys('aaaaa')
        new_pw2.send_keys('aaaaa')
        driver.find_element_by_xpath('//*[@id="changePwForm"]/div[4]/div/div/input').click()

    '''
    Help function signing up already existing user (email).
    '''
    def try_dupe(self, driver, email, button):
        email.send_keys('matilda@gmail.com')
        button.click()
        try:
            WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="error"]'))
            )
        finally:
            element = self.verify_error(driver)
            assert 'already exists' in element.text
    '''
    Help function to try if blank form can be signed up.
    '''
    def try_blank_form(self, driver, button):
        button.click()
        try:
            WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="error"]'))
            )
        finally:
            element = self.verify_error(driver)
            assert element.text != 'Signed up'

    '''
    Help function to verify that error message is displayed.
    '''
    def verify_error(self, driver):
        try:
            element = driver.find_element_by_xpath('//*[@id="error"]')
        except IOError:
            element = None

        assert element is not None
        return element

    '''
    Help function to try to change with wrong pw.
    '''
    def try_wrong_password(self, driver, password, repeat, button, email):
        repeat.send_keys('wrongpwd')
        button.click()
        try:
            WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="error"]'))
            )
        finally:
            element = self.verify_error(driver)
            assert 'password failed' in element.text

    '''
    Help function to post a message to wall.
    '''
    def post_help(self, driver, message, text_area, tab):
        text_area.send_keys(message)
        post_button = driver.find_element_by_xpath(tab)
        post_button.click()

        try:
            WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="' + message +'"]/textarea'))
            )
        finally:
            assert message in driver.find_element_by_xpath('//*[@id="' + message + '"]/textarea').text


    '''
    Help function to log in before tests.
    '''
    def log_in_help(self, driver, email_string, pw_string):
        email = driver.find_element_by_xpath('//*[@id="loginemail"]')
        pw = driver.find_element_by_xpath('//*[@id="loginpassword"]')
        login_button = driver.find_element_by_xpath('//*[@id="loginButton"]')
        email.send_keys(email_string)
        pw.send_keys(pw_string)
        login_button.click()
        time.sleep(1)
        try:
            WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="useremail"]')))
        finally:
            assert email_string in driver.find_element_by_xpath('//*[@id="useremail"]').text



    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()