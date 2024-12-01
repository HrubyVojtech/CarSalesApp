import pytest
from ..Calculator import Calculator
from ..CarSalesUI import CarSalesUI
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

# Vytvoříme instanci QApplication, což je základní nutnost pro PyQt aplikace
@pytest.fixture
def app():
    app = QApplication(sys.argv)
    return app

# Test inicializace třídy Calculator
def test_calculator_initialization(app):
    # Nejprve vytvoříme instanci UI, kterou pak předáme Calculatoru
    main_window = QMainWindow()
    ui = CarSalesUI(main_window)
    calculator = Calculator(ui)
    
    # Zkontrolujeme, zda se instance Calculator vytvořila správně
    assert calculator.ui == ui

# Test funkce calculate_total pro platné vstupy
def test_calculate_total_valid(app):
    main_window = QMainWindow()
    ui = CarSalesUI(main_window)
    calculator = Calculator(ui)

    # Představujeme si, že máme nějaká testovací data o autech
    class MockCar:
        def __init__(self, model, sale_date, price):
            self.model = model
            self.sale_date = sale_date
            self.price = price

        def get_price(self):
            return self.price

    cars = [
        MockCar("Škoda Octavia", "2020.12.04", 500000),
        MockCar("Škoda Superb", "2020.12.05", 600000)
    ]

    # Nastavíme hodnoty v UI tak, aby simulovaly vstupy od uživatele
    ui.year_input.setCurrentText("2020")
    ui.model_filter.setCurrentText("Všechny modely")

    # Zavoláme metodu calculate_total
    calculator.calculate_total(cars)

    # Ověříme, že výsledek je správně zobrazen
    expected_total = (500000 + 600000) * 1.21
    assert ui.total_label.text() == f'Celková cena s DPH: {expected_total:,.2f} Kč'

# Test funkce calculate_total pro neplatný rok
def test_calculate_total_invalid_year(app):
    main_window = QMainWindow()
    ui = CarSalesUI(main_window)
    calculator = Calculator(ui)

    cars = []  # Můžeme použít prázdný seznam, protože rok je neplatný

    # Nastavíme hodnoty v UI tak, aby simulovaly neplatný vstup
    ui.year_input.setCurrentText("neplatný rok")

    # Zavoláme metodu calculate_total
    calculator.calculate_total(cars)

    # Ověříme, že správně zobrazí zprávu o neplatném roku
    assert ui.total_label.text() == "Prosím, zadejte platný rok."


# Test funkce calculate_total s filtrem podle modelu
def test_calculate_total_filter_by_model(app):
    main_window = QMainWindow()
    ui = CarSalesUI(main_window)
    calculator = Calculator(ui)

    # Mockovací auta
    class MockCar:
        def __init__(self, model, sale_date, price):
            self.model = model
            self.sale_date = sale_date
            self.price = price

        def get_price(self):
            return self.price

    cars = [
        MockCar("Škoda Octavia", "2020.12.04", 500000),
        MockCar("Škoda Superb", "2020.12.05", 600000),
        MockCar("Škoda Octavia", "2020.12.06", 550000),
    ]

    # Nastavíme hodnoty v UI tak, aby simulovaly vstupy od uživatele
    ui.year_input.setCurrentText("2020")
    ui.model_filter.clear()
    ui.model_filter.addItem("Všechny modely")
    ui.model_filter.addItem("Škoda Octavia")
    ui.model_filter.addItem("Škoda Superb")
    ui.model_filter.setCurrentText("Škoda Octavia")

    # Diagnostický výpis pro kontrolu hodnoty
    print(f"Vybraný rok: {ui.year_input.currentText()}")
    print(f"Vybraný model: {ui.model_filter.currentText()}")

    # Zavoláme metodu calculate_total
    calculator.calculate_total(cars)

    # Ověříme, že výsledek obsahuje pouze auta "Škoda Octavia"
    expected_total = (500000 + 550000) * 1.21
    assert ui.total_label.text() == f'Celková cena s DPH: {expected_total:,.2f} Kč'

# Test funkce calculate_total pro prázdný seznam aut
def test_calculate_total_empty_cars_list(app):
    main_window = QMainWindow()
    ui = CarSalesUI(main_window)
    calculator = Calculator(ui)

    # Prázdný seznam aut
    cars = []

    # Nastavíme hodnoty v UI tak, aby simulovaly platný vstup od uživatele
    ui.year_input.setCurrentText("2020")
    ui.model_filter.setCurrentText("Všechny modely")

    # Zavoláme metodu calculate_total
    calculator.calculate_total(cars)

    # Ověříme, že výsledek pro prázdný seznam aut je správně zobrazen (0 Kč)
    expected_total = 0 * 1.21
    assert ui.total_label.text() == f'Celková cena s DPH: {expected_total:,.2f} Kč'

# Test funkce calculate_total pro neexistující kombinaci roku a modelu
def test_calculate_total_no_matching_cars(app):
    main_window = QMainWindow()
    ui = CarSalesUI(main_window)
    calculator = Calculator(ui)

    # Mockovací auta
    class MockCar:
        def __init__(self, model, sale_date, price):
            self.model = model
            self.sale_date = sale_date
            self.price = price

        def get_price(self):
            return self.price

    cars = [
        MockCar("Škoda Octavia", "2019.12.04", 500000),
        MockCar("Škoda Superb", "2021.12.05", 600000),
        MockCar("Škoda Octavia", "2021.12.06", 550000),
    ]

    # Nastavíme rok a model, které v seznamu aut neexistují
    ui.year_input.setCurrentText("2020")
    ui.model_filter.clear()
    ui.model_filter.addItem("Všechny modely")
    ui.model_filter.addItem("Škoda Octavia")
    ui.model_filter.addItem("Škoda Superb")
    ui.model_filter.setCurrentText("Škoda Octavia")

    # Zavoláme metodu calculate_total
    calculator.calculate_total(cars)

    # Ověříme, že výsledek je 0, protože neexistují žádná auta z roku 2020
    expected_total = 0 * 1.21
    assert ui.total_label.text() == f'Celková cena s DPH: {expected_total:,.2f} Kč'
 
 # Test funkce calculate_total pro auta s neplatnými cenami
def test_calculate_total_invalid_prices(app):
    main_window = QMainWindow()
    ui = CarSalesUI(main_window)
    calculator = Calculator(ui)

    # Mockovací auta s neplatnými cenami
    class MockCar:
        def __init__(self, model, sale_date, price):
            self.model = model
            self.sale_date = sale_date
            self.price = price

        def get_price(self):
            # Pokud cena není číslo, vracíme 0
            if self.price is None:
                return 0.0
            try:
                return float(self.price)
            except ValueError:
                return 0.0

    cars = [
        MockCar("Škoda Octavia", "2020.12.04", 500000),   # Platná cena
        MockCar("Škoda Superb", "2020.12.05", "neplatná"), # Neplatná cena
        MockCar("Škoda Octavia", "2020.12.06", None),      # Chybějící cena
        MockCar("Škoda Fabia", "2020.12.07", 300000)       # Platná cena
    ]

    # Nastavíme hodnoty v UI tak, aby simulovaly vstupy od uživatele
    ui.year_input.setCurrentText("2020")
    ui.model_filter.setCurrentText("Všechny modely")

    # Zavoláme metodu calculate_total
    calculator.calculate_total(cars)

    # Ověříme, že výsledek obsahuje pouze auta s platnými cenami
    expected_total = (500000 + 300000) * 1.21
    assert ui.total_label.text() == f'Celková cena s DPH: {expected_total:,.2f} Kč'