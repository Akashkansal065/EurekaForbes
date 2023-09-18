from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.service import Service as ChromeService
import json
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException, \
    ElementClickInterceptedException, ElementNotInteractableException, WebDriverException, InvalidSelectorException

firefoxpath = "/Users/akash.kansal/Documents/GitHub/cypress/checkout_automation_api/resources/geckodriver"
chromepath = "/Users/akash.kansal/Documents/GitHub/cypress/checkout_automation_api/resources/chromemac1"


class Eureka:
    def __init__(self, browser, executionPlatform) -> None:
        self.browser = browser
        self.executionPlatform = executionPlatform
        f = open(
            '/Users/akash.kansal/Documents/GitHub/cypress/checkout_automation_api/Extras/path.json')
        data = json.load(f)
        self.pathmaps = {}
        self.pathmaps = data[str(self.executionPlatform).casefold()]
        f.close()

    def launchbrowser(self):

        if str(self.browser.casefold()) == 'chrome':
            desired_cap = webdriver.DesiredCapabilities.CHROME.copy()
            desired_cap['browserName'] = 'chrome'
            # opt = webdriver.ChromeOptions()
            opt = webdriver.ChromeOptions()
            opt.add_argument("no-sandbox")
            opt.set_capability("acceptInsecureCerts", True)
            opt.add_argument('--allow-running-insecure-content')
            opt.add_argument('--ignore-certificate-errors')
            opt.add_argument("--ignore-certificate-errors-spki-list")
            opt.add_argument('disable-infobars')
            opt.add_argument('--ignore-ssl-errors')
            opt.add_argument("--disable-gpu")
            opt.add_argument("--disable-dev-shm-usage")
            opt.add_argument("--disable-notifications")
            opt.add_argument('-suppress-message-center-popups')
            opt.add_argument("--disable-notifications")
            prefs = {"profile.default_content_setting_values.notifications": 2}
            service = ChromeService(executable_path=chromepath)
            service.start()
            opt.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
            if self.executionPlatform == "WEBSITE":
                opt.add_experimental_option("prefs", prefs)
                self.driver = webdriver.Chrome(
                    service=service, options=opt)
                self.driver.maximize_window()
                self.driver.implicitly_wait(15)
                return self.driver

            if self.executionPlatform == "MSITE":
                opt.add_argument(
                    '--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 '
                    '(KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1')

                opt.add_experimental_option("prefs", prefs)
                self.driver = webdriver.Chrome(
                    executable_path=chromepath, options=opt)
                self.driver.set_window_size(500, 900)
                return self.driver
        if str(self.browser.casefold()) == 'firefox':
            desired_cap = DesiredCapabilities.FIREFOX.copy()
            desired_cap['acceptInsecureCerts'] = True
            desired_cap['javascriptEnabled'] = True
            desired_cap['browserName'] = 'firefox'
            # desired_cap['deviceName'] = 'iPhone X'
            opt = webdriver.FirefoxOptions()
            opt.add_argument("--start-maximized")
            swoptions = {
                'disable_encoding': True,
                'verify_ssl': False
            }
            service = FirefoxService(executable_path=firefoxpath)
            service.start()

            # if plat.system() == "Windows":
            # opt.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'

            if self.executionPlatform == "WEBSITE":
                self.driver = webdriver.Firefox(
                    executable_path=firefoxpath, options=opt)
                self.driver.maximize_window()
                self.driver.implicitly_wait(15)
                return self.driver

            if self.executionPlatform == "MSITE":
                useragent = "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
                opt.set_preference('general.useragent.override', useragent)
                opt.set_capability('acceptInsecureCerts', True)
                opt.set_capability('javascriptEnabled', True)
                opt.set_capability('browserName', 'firefox')
                opt.add_argument('--width=360')
                opt.add_argument('--height=640')
                opt.add_argument(
                    '--user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"')

                self.driver = webdriver.Firefox(service=service, options=opt)
                self.driver.set_window_size(500, 900)
                return self.driver

    def launchsite(self):
        self.driver.get("https://www.eurekaforbes.com/")

    def quit(self):
        self.driver.close()

    def openService(self):
        Eureka.clickonelement(self, self.pathmaps['service'])

    def clickonelement(self, element):
        self.driver.find_element(
            by=By.CSS_SELECTOR, value=element).click()

    def sendKeysAll(self, element, text):
        self.driver.find_element(
            by=By.CSS_SELECTOR, value=element).send_keys(text)

    def bookService(self):
        element = self.driver.find_element(
            by=By.CSS_SELECTOR, value=self.pathmaps['bookServiceWidgetForScroll'])
        Eureka.scrollToElement(self, element)
        element = self.driver.find_element(
            by=By.CSS_SELECTOR, value=self.pathmaps['bookService'])
        Eureka.click_action(self, element)

    def login(self):
        element = self.driver.find_element(
            by=By.CSS_SELECTOR, value=self.pathmaps['mobileField'])
        Eureka.click_action(self, element)
        Eureka.sendKeysAll(self, self.pathmaps['mobileField'], "9873603803")
        Eureka.click_action(self, self.driver.find_element(
            by=By.CSS_SELECTOR, value=self.pathmaps['submitLogin']))

    def submitAndVerifyOtp(self):
        Eureka.click_action(self, self.driver.find_element(
            by=By.CSS_SELECTOR, value=self.pathmaps['otp']))
        Eureka.sendKeysAll(self, self.pathmaps['otp'], "123456")
        Eureka.click_action(self, self.driver.find_element(
            by=By.CSS_SELECTOR, value=self.pathmaps['submitOtp']))

    def waitForElementPresent(self, selector, time):
        try:
            WebDriverWait(self.driver, time).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, selector)))
            return True
        except (NoSuchElementException, InvalidSelectorException, TimeoutException):
            return False

    def userSuccessLoggedIn(self):
        Eureka.waitForElementPresent(
            self, self.pathmaps['serviceRequestButton'], 20)

    def scrollToElement(self, element):
        self.driver.execute_script(
            "return arguments[0].scrollIntoView(true);", element)

    def scrollDown(self, length):
        self.driver.execute_script(f"window.scrollTo(0, {length});")

    def click_action(self, element):
        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)
        except ElementNotInteractableException:
            time.sleep(5)
            self.driver.execute_script("arguments[0].click();", element)
        except WebDriverException:
            if Eureka.isElementPresent(self, self.driver, element):
                self.driver.execute_script("arguments[0].click();", element)
        except Exception:
            actions = ActionChains(self.driver)
            actions.move_to_element(element).click().perform()

    def isElementPresent(self, driver, selector):
        try:
            self.driver.find_element(selector)
            return True
        except (TimeoutException, NoSuchElementException, Exception) as e:
            return False


# eu = Eureka("chrome", "MSITE")
eu = Eureka("chrome", "WEBSITE")
eu.launchbrowser()
eu.launchsite()
eu.openService()
eu.bookService()
eu.login()
eu.submitAndVerifyOtp()
eu.userSuccessLoggedIn()
eu.quit()
