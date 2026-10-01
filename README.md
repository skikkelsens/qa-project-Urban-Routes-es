# QA Project: Urban Routes (Page Object Model)

## Descripción

Suite de pruebas automatizadas para la aplicación web **Urban Routes**, un servicio de pedido de taxis. 
El proyecto cubre el flujo completo de un pedido de principio a fin, 
siguiendo el patrón de diseño **Page Object Model (POM)** para mantener los localizadores y las acciones 
de la interfaz separados de la lógica de las pruebas.

El flujo probado incluye:

1. Configurar la dirección de origen y destino.
2. Seleccionar la tarifa **Comfort**.
3. Rellenar el número de teléfono y confirmarlo mediante el código de verificación SMS.
4. Agregar una tarjeta de crédito como método de pago.
5. Escribir un mensaje para el conductor.
6. Solicitar manta y pañuelos.
7. Pedir 2 helados.
8. Verificar que aparece el modal de búsqueda de taxi.
9. Esperar a que se asigne un conductor y se muestre su información en el modal.

## Tecnologías y técnicas utilizadas

**Python** como lenguaje de programación.
**Selenium WebDriver** para la automatización del navegador (Chrome).
**pytest** como framework de pruebas.
**Page Object Model (POM)**: la clase `UrbanRoutesPage` encapsula todos los localizadores 
  - y las interacciones con la interfaz, mientras que la clase `TestUrbanRoutes` contiene únicamente 
  - la lógica de las pruebas.
**Esperas explícitas** (`WebDriverWait` + `expected_conditions`) en lugar de `time.sleep()`, 
  - usando las condiciones adecuadas según el tipo de interacción 
  - (`element_to_be_clickable`, `visibility_of_element_located`, 
  - `presence_of_element_located`, `presence_of_all_elements_located`).
**Localizadores XPath y CSS** cuidadosamente acotados para evitar colisiones entre elementos 
  - que comparten clases o IDs genéricos (por ejemplo, modales superpuestos o campos 
  - reutilizados en distintas pantallas).
**Interceptación de logs de red** (`goog:loggingPrefs`) para capturar el código de verificación 
  - del teléfono mediante la función `retrieve_phone_code`.
**Métodos combinadores** (por ejemplo, `set_route`, `add_credit_card`, `order_two_ice_creams`) 
  - que agrupan varias acciones atómicas en un solo paso reutilizable.
**Helpers de configuración reutilizables** dentro de la clase de pruebas 
  - (`_select_route_and_comfort`, `_verify_phone`, `_add_card`) 
  - para evitar la repetición de código entre pruebas, manteniendo cada prueba independiente 
  - y capaz de ejecutarse de forma aislada.

## Estructura del proyecto

```
qa-project-Urban-Routes-es/
├── data/
│   └── data.py              # Datos de prueba (URL, direcciones, teléfono, tarjeta, mensaje)
├── pages/
│   └── urban_routes_pg.py   # Page Object: localizadores y métodos de interacción
├── Tests/
│   └── Test_urban_routes.py # Casos de prueba
├── utils/
│   └── retrieve_code.py     # Función para recuperar el código de confirmación por SMS
└── README.md
```

## Cómo ejecutar las pruebas

### Requisitos previos

- Python 3.10 o superior.
- Google Chrome instalado.
- Las dependencias del proyecto instaladas en un entorno virtual:

```bash
python -m venv .venv
.venv\Scripts\activate        # En Windows
# source .venv/bin/activate   # En macOS/Linux

pip install selenium pytest
```

### Configuración

Antes de ejecutar las pruebas, verifica que la URL del entorno de pruebas en `data/data.py` 
esté activa y actualizada, ya que el contenedor de prueba puede expirar o 
cambiar de dirección con el tiempo:

```python
urban_routes_url = "https://tu-url-actual.containerhub.tripleten-services.com/"
```

### Ejecutar toda la suite de pruebas

Desde la raíz del proyecto:

```bash
pytest Tests/Test_urban_routes.py -v
```

### Ejecutar una prueba específica

```bash
pytest Tests/Test_urban_routes.py::TestUrbanRoutes::test_4_add_credit_card -v
```

### Notas

- Cada prueba abre y cierra su propia instancia del navegador (`setup_method` / `teardown_method`)
- por lo que todas las pruebas son independientes entre sí y pueden ejecutarse en cualquier orden 
- o de forma aislada.  
- La prueba `test_9_wait_for_driver_assigned` puede tardar hasta 60 segundos, ya que depende 
- de la simulación de asignación de un conductor dentro de la aplicación.
