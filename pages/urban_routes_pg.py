
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from utils.retrieve_code import retrieve_phone_code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    request_taxi_button = (By.CSS_SELECTOR, '.button.round')
    comfort_selector = (By.XPATH, '//div[@class="tcard-title" and text()="Comfort"]')
    comfort_selector_assert = (By.CSS_SELECTOR, '.tcard.active .tcard-title')
    phone_field = (By.XPATH, '//div[@class="np-text" and text()="Phone number"]')
    phone_number_field = (By.ID, 'phone')
    next_button = (By.XPATH, '//button[text()="Next"]')
    phone_code_field = (By.ID, 'code')
    confirm_button = (By.XPATH, '//button[text()="Confirm"]')
    payment_method_field = (By.XPATH, '//div[@class="pp-text" and text()="Método de pago"]')


    def __init__(self, driver):
        self.card_cvv_field = None
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def set_from(self, from_address):
        self.wait.until(EC.visibility_of_element_located(self.from_field)
          ).send_keys(from_address)

    def set_to(self, to_address):
        self.wait.until(EC.visibility_of_element_located(self.to_field)
        ).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self, address_from, address_to):
        self.set_from(address_from)
        self.set_to(address_to)

    def get_request_taxi_button(self):
        return self.wait.until(
            EC.element_to_be_clickable(self.request_taxi_button)
        )

    def click_request_taxi_button(self):
        self.get_request_taxi_button().click()

    def get_comfort_selector(self):
        return self.wait.until(
            EC.element_to_be_clickable(self.comfort_selector)
        )

    def click_comfort_selector(self):
        self.get_comfort_selector().click()

    def get_comfort_selector_assert(self):
        return self.wait.until(EC.presence_of_element_located(
            self.comfort_selector_assert)
        )

    def get_phone_field(self):
        return self.wait.until(EC.element_to_be_clickable(self.phone_field))

    def click_phone_field(self):
        self.get_phone_field().click()

    def set_phone_number(self, phone_number):
        self.wait.until(
            EC.visibility_of_element_located(self.phone_number_field)
        ).send_keys(phone_number)

    def get_next_button(self):
        return self.wait.until(EC.element_to_be_clickable(self.next_button))

    def click_next_button(self):
        self.get_next_button().click()

    def set_phone_code(self, code):
        self.wait.until(
            EC.visibility_of_element_located(self.phone_code_field)
        ).send_keys(code)


    def get_confirm_button(self):
        return self.wait.until(EC.element_to_be_clickable(self.confirm_button))

    def click_confirm_button(self):
        self.get_confirm_button().click()

    def get_payment_method_field(self):
        return self.wait.until(EC.element_to_be_clickable(self.payment_method_field))

    def click_payment_method_field(self):
        self.get_payment_method_field().click()

    def set_card_cvv(self, card_code):
        field = self.wait.until(
            EC.visibility_of_element_located(self.card_cvv_field)
        )
        field.send_keys(card_code)
        field.send_keys(Keys.TAB)

    def add_credit_card(self, card_number, card_code):
        pass