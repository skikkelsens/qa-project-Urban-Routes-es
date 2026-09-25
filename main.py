
import data
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    request_taxi_button = (By.CSS_SELECTOR, '.button.round')
    comfort_selector = (By.XPATH, '//div[@class="tcard-title" and text()="Comfort"]')
    comfort_selector_assert = (By.CSS_SELECTOR, '.tcard.active .tcard-title')


    def __init__(self, driver):
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

class TestUrbanRoutes:

    def setup_method(self):
        options = Options()
        options.set_capability("goog:loggingPrefs", {'performance':'ALL'})
        self.driver = webdriver.Chrome(service=Service(), options=options)
        self.driver.get(data.urban_routes_url)
        self.routes_page = UrbanRoutesPage(self.driver)
        self.address_from = data.address_from
        self.address_to = data.address_to

    def test_1_set_route(self):
        self.routes_page.set_route(self.address_from, self.address_to)
        assert self.routes_page.get_from() == self.address_from
        assert self.routes_page.get_to() == self.address_to

    def test_2_select_comfort(self):
        self.routes_page.set_route(self.address_from, self.address_to)
        self.routes_page.click_request_taxi_button()
        self.routes_page.click_comfort_selector()

        comfort_tariff = self.routes_page.get_comfort_selector_assert().text
        assert comfort_tariff == "Comfort"

    def teardown_method(self):
        self.driver.quit()
