from data import data
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from pages.urban_routes_pg import UrbanRoutesPage
from utils.retrieve_code import retrieve_phone_code


class TestUrbanRoutes:

    def setup_method(self):
        options = Options()
        options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        self.driver = webdriver.Chrome(service=Service(), options=options)
        self.driver.get(data.urban_routes_url)
        self.routes_page = UrbanRoutesPage(self.driver)
        self.address_from = data.address_from
        self.address_to = data.address_to

    # --- Helpers: checkpoints reutilizables del flujo ---

    def _select_route_and_comfort(self):
        self.routes_page.set_route(self.address_from, self.address_to)
        self.routes_page.click_request_taxi_button()
        self.routes_page.click_comfort_selector()

    def _verify_phone(self):
        self._select_route_and_comfort()
        self.routes_page.click_phone_field()
        self.routes_page.set_phone_number(data.phone_number)
        self.routes_page.click_next_button()
        code = retrieve_phone_code(self.driver)
        self.routes_page.set_phone_code(code)
        self.routes_page.click_confirm_button()

    def _add_card(self):
        self._verify_phone()
        self.routes_page.add_credit_card(data.card_number, data.card_code)
        self.routes_page.click_close_payment_modal_button()

    # --- Pruebas ---

    # Prueba 1. Configurar la dirección
    def test_1_set_route(self):
        self.routes_page.set_route(self.address_from, self.address_to)
        assert self.routes_page.get_from() == self.address_from
        assert self.routes_page.get_to() == self.address_to

    # Prueba 2. Seleccionar la tarifa Comfort
    def test_2_select_comfort(self):
        self._select_route_and_comfort()
        comfort_tariff = self.routes_page.get_comfort_selector_assert().text
        assert comfort_tariff == "Comfort"

    # Prueba 3. Rellenar número de teléfono
    def test_3_fill_ph_numbr(self):
        self._verify_phone()

    # Prueba 4. Agregar una tarjeta de crédito
    def test_4_add_credit_card(self):
        self._verify_phone()
        self.routes_page.add_credit_card(data.card_number, data.card_code)
        assert self.routes_page.is_card_selected() is True
        self.routes_page.click_close_payment_modal_button()

    # Prueba 5. Escribir un mensaje para el conductor
    def test_5_write_message_for_driver(self):
        self._add_card()
        self.routes_page.set_driver_message(data.message_for_driver)
        assert self.routes_page.get_driver_message() == data.message_for_driver

    # Prueba 6. Pedir una manta y pañuelos
    def test_6_order_blanket_and_tissues(self):
        self._add_card()
        self.routes_page.set_driver_message(data.message_for_driver)
        self.routes_page.click_blanket_tissues_checkbox()
        assert self.routes_page.is_blanket_tissues_selected() is True

    # Prueba 7. Pedir 2 helados
    def test_7_order_two_ice_creams(self):
        self._add_card()
        self.routes_page.set_driver_message(data.message_for_driver)
        self.routes_page.click_blanket_tissues_checkbox()
        self.routes_page.order_two_ice_creams()
        assert self.routes_page.get_ice_cream_count() == '2'

    # Prueba 8. Aparece el modal para buscar un taxi
    def test_8_order_taxi_modal_appears(self):
        self._add_card()
        self.routes_page.set_driver_message(data.message_for_driver)
        self.routes_page.click_blanket_tissues_checkbox()
        self.routes_page.order_two_ice_creams()
        self.routes_page.click_order_taxi_button()
        assert self.routes_page.is_searching_taxi_modal_visible() is True

    # Prueba 9. Esperar a que aparezca la información del conductor en el modal
    def test_9_wait_for_driver_assigned(self):
        self._add_card()
        self.routes_page.set_driver_message(data.message_for_driver)
        self.routes_page.click_blanket_tissues_checkbox()
        self.routes_page.order_two_ice_creams()
        self.routes_page.click_order_taxi_button()
        assert self.routes_page.is_driver_assigned() is True

    def teardown_method(self):
        self.driver.quit()