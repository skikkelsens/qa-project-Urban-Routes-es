
from data import data
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from pages.urban_routes_pg import UrbanRoutesPage
from utils.retrieve_code import retrieve_phone_code


class TestUrbanRoutes:

    def setup_method(self):
        options = Options()
        options.set_capability("goog:loggingPrefs", {'performance':'ALL'})
        self.driver = webdriver.Chrome(service=Service(), options=options)
        self.driver.get(data.urban_routes_url)
        self.routes_page = UrbanRoutesPage(self.driver)
        self.address_from = data.address_from
        self.address_to = data.address_to

# Prueba 1. Configurar la dirección
    def test_1_set_route(self):
        self.routes_page.set_route(self.address_from, self.address_to)
        assert self.routes_page.get_from() == self.address_from
        assert self.routes_page.get_to() == self.address_to

# Prueba 2. Seleccionar la tarifa Comfort
    def test_2_select_comfort(self):
        self.routes_page.set_route(self.address_from, self.address_to)
        self.routes_page.click_request_taxi_button()
        self.routes_page.click_comfort_selector()

        comfort_tariff = self.routes_page.get_comfort_selector_assert().text
        assert comfort_tariff == "Comfort"

# Prueba 3. Rellenar número de teléfono
    def test_3_fill_ph_numbr(self):
        self.routes_page.set_route(self.address_from, self.address_to)
        self.routes_page.click_request_taxi_button()
        self.routes_page.click_comfort_selector()
        self.routes_page.click_phone_field()
        self.routes_page.set_phone_number(data.phone_number)
        self.routes_page.click_next_button()
        self.routes_page.set_phone_code(code)
        self.routes_page.click_confirm_button()

# Prueba 4.
    def test_4_add_credit_card(self):
        self.routes_page.set_route(self.address_from, self.address_to)
        self.routes_page.click_request_taxi_button()
        self.routes_page.click_comfort_selector()
        self.routes_page.click_phone_field()
        self.routes_page.set_phone_number(data.phone_number)
        self.routes_page.click_next_button()
        self.routes_page.set_phone_code(code)
        self.routes_page.click_confirm_button()

        self.routes_page.add_credit_card(data.card_number, data.card_code)


    def teardown_method(self):
        self.driver.quit()
