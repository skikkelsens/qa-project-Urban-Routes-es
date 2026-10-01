from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys



class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    request_taxi_button = (By.CSS_SELECTOR, '.button.round')
    comfort_selector = (By.XPATH, '//div[@class="tcard-title" and text()="Comfort"]')
    comfort_selector_assert = (By.CSS_SELECTOR, '.tcard.active .tcard-title')
    phone_field = (By.XPATH, '//div[@class="np-text" and text()="Número de teléfono"]')
    phone_number_field = (By.ID, 'phone')
    next_button = (By.XPATH, '//button[text()="Siguiente"]')
    phone_code_field = (By.ID, 'code')
    confirm_button = (By.XPATH, '//button[text()="Confirmar"]')
    payment_method_field = (By.XPATH, '//div[@class="pp-text" and text()="Método de pago"]')
    add_card_link = (By.XPATH, '//div[@class="pp-title" and text()="Agregar tarjeta"]')
    card_number_field = (By.ID, 'number')
    card_cvv_field = (By.CSS_SELECTOR, '#code.card-input')
    add_card_button = (By.XPATH, '//button[text()="Agregar"]')
    card_added_checkbox = (By.ID, 'card-1')
    close_payment_modal_button = (By.CSS_SELECTOR, '.close-button.section-close')
    driver_message_field = (By.ID, 'comment')
    blanket_tissues_checkbox = (By.XPATH,'//div[@class="r-sw-label" and text()="Manta y pañuelos"]'
                                '/following-sibling::div[@class="r-sw"]//input[@class="switch-input"]'
                                )
    blanket_tissues_slider = (By.XPATH,'//div[@class="r-sw-label" and text()="Manta y pañuelos"]'
                                '/following-sibling::div[@class="r-sw"]//span[@class="slider round"]'
                                )
    ice_cream_plus_button = (
        By.XPATH,
        '//div[@class="r-counter-label" and text()="Helado"]/following-sibling::div[@class="r-counter"]//div[contains(@class,"counter-plus")]'
    )
    ice_cream_counter_value = (
        By.XPATH,
        '//div[@class="r-counter-label" and text()="Helado"]/following-sibling::div[@class="r-counter"]//div[@class="counter-value"]'
    )
    order_taxi_button = (By.XPATH, '//span[@class="smart-button-main" and text()="Pedir un taxi"]/parent::button')
    searching_taxi_title = (By.XPATH, '//div[@class="order-header-title" and text()="Buscar automóvil"]')
    driver_rating = (By.CLASS_NAME, 'order-btn-rating')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def set_from(self, from_address):
        self.wait.until(EC.visibility_of_element_located(self.from_field)).send_keys(from_address)

    def set_to(self, to_address):
        self.wait.until(EC.visibility_of_element_located(self.to_field)).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self, address_from, address_to):
        self.set_from(address_from)
        self.set_to(address_to)

    def get_request_taxi_button(self):
        return self.wait.until(EC.element_to_be_clickable(self.request_taxi_button))

    def click_request_taxi_button(self):
        self.get_request_taxi_button().click()

    def get_comfort_selector(self):
        return self.wait.until(EC.element_to_be_clickable(self.comfort_selector))

    def click_comfort_selector(self):
        self.get_comfort_selector().click()

    def get_comfort_selector_assert(self):
        return self.wait.until(EC.presence_of_element_located(self.comfort_selector_assert))

    def get_phone_field(self):
        return self.wait.until(EC.element_to_be_clickable(self.phone_field))

    def click_phone_field(self):
        self.get_phone_field().click()

    def set_phone_number(self, phone_number):
        self.wait.until(EC.visibility_of_element_located(self.phone_number_field)).send_keys(phone_number)

    def get_next_button(self):
        return self.wait.until(EC.element_to_be_clickable(self.next_button))

    def click_next_button(self):
        self.get_next_button().click()

    def set_phone_code(self, code):
        self.wait.until(EC.visibility_of_element_located(self.phone_code_field)).send_keys(code)

    def get_confirm_button(self):
        return self.wait.until(EC.element_to_be_clickable(self.confirm_button))

    def click_confirm_button(self):
        self.get_confirm_button().click()

    def get_payment_method_field(self):
        return self.wait.until(EC.element_to_be_clickable(self.payment_method_field))

    def click_payment_method_field(self):
        self.get_payment_method_field().click()

    def get_add_card_link(self):
        return self.wait.until(EC.element_to_be_clickable(self.add_card_link))

    def click_add_card_link(self):
        self.get_add_card_link().click()

    def set_card_number(self, card_number):
        self.wait.until(EC.visibility_of_element_located(self.card_number_field)).send_keys(card_number)

    def set_card_cvv(self, card_code):
        field = self.wait.until(EC.visibility_of_element_located(self.card_cvv_field))
        field.send_keys(card_code)
        field.send_keys(Keys.TAB)

    def get_add_card_button(self):
        return self.wait.until(EC.element_to_be_clickable(self.add_card_button))

    def click_add_card_button(self):
        self.get_add_card_button().click()

    def add_credit_card(self, card_number, card_code):
        self.click_payment_method_field()
        self.click_add_card_link()
        self.set_card_number(card_number)
        self.set_card_cvv(card_code)
        self.click_add_card_button()

    def is_card_selected(self):
        checkbox = self.wait.until(
            EC.presence_of_element_located(self.card_added_checkbox)
        )
        return checkbox.is_selected()

    def click_close_payment_modal_button(self):
        buttons = self.wait.until(
            EC.presence_of_all_elements_located(self.close_payment_modal_button)
        )
        for button in buttons:
            if button.is_displayed() and button.is_enabled():
                button.click()
                return
        raise Exception("No se encontró ningún botón de cierre visible del modal de pago")

    def set_driver_message(self, message):
        self.wait.until(
            EC.visibility_of_element_located(self.driver_message_field)
        ).send_keys(message)

    def get_driver_message(self):
        return self.driver.find_element(*self.driver_message_field).get_property('value')

    def click_blanket_tissues_checkbox(self):
        self.wait.until(EC.element_to_be_clickable(self.blanket_tissues_slider)).click()

    def is_blanket_tissues_selected(self):
        return self.driver.find_element(*self.blanket_tissues_checkbox).is_selected()

    def click_ice_cream_plus_button(self):
        self.wait.until(EC.element_to_be_clickable(self.ice_cream_plus_button)).click()

    def order_two_ice_creams(self):
        self.click_ice_cream_plus_button()
        self.click_ice_cream_plus_button()

    def get_ice_cream_count(self):
        return self.driver.find_element(*self.ice_cream_counter_value).text

    def get_order_taxi_button(self):
        return self.wait.until(EC.element_to_be_clickable(self.order_taxi_button))

    def click_order_taxi_button(self):
        self.get_order_taxi_button().click()

    def is_searching_taxi_modal_visible(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.searching_taxi_title)
        ).is_displayed()

    def wait_for_driver_assigned(self):
        return WebDriverWait(self.driver, 60).until(
            EC.visibility_of_element_located(self.driver_rating)
        )

    def is_driver_assigned(self):
        return self.wait_for_driver_assigned().is_displayed()