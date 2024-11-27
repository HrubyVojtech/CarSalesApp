import pytest
from ..Car import Car

def test_car_initialization():
    # Test, že se auto inicializuje správně
    car = Car("Škoda Octavia", "4.12.2020", 500000)
    assert car.model == "Škoda Octavia"
    assert car.sale_date == "4.12.2020"
    assert car.price == 500000

def test_get_price():
    # Test metody get_price pro správnou hodnotu
    car = Car("Škoda Octavia", "4.12.2020", 500000)
    assert car.get_price() == 500000.0

    # Test metody get_price pro neplatnou hodnotu ceny
    car = Car("Škoda Octavia", "4.12.2020", "neplatná hodnota")
    assert car.get_price() == 0.0
