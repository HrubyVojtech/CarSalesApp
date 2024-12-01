import pytest
from DataLoader import JsonDataLoader
from DataLoader import XmlDataLoader
from Car import Car
import os

# Test načítání dat ze souboru JSON pomocí JsonDataLoader
def test_json_data_loader(tmp_path):
    # Vytvoříme dočasný JSON soubor s testovacími daty
    data = [
        {
            "Název modelu": "Škoda Octavia",
            "Datum prodeje": "4.12.2020",
            "Cena bez DPH": 500000
        },
        {
            "Název modelu": "Škoda Superb",
            "Datum prodeje": "5.12.2019",
            "Cena bez DPH": "neplatná"
        },
        {
            "Název modelu": "Škoda Fabia",
            "Datum prodeje": "6.12.2018",
            "Cena bez DPH": 300000
        }
    ]
    
    file_path = tmp_path / "test_data.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        import json
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    # Načteme data pomocí JsonDataLoader
    loader = JsonDataLoader()
    cars = loader.load_data(str(file_path))

    # Ověříme, že data byla správně načtena
    assert len(cars) == 3
    assert isinstance(cars[0], Car)
    assert cars[0].model == "Škoda Octavia"
    assert cars[0].sale_date == "2020.12.04"  # Datum je převedeno na formát YYYY.MM.DD
    assert cars[0].price == 500000

    # Kontrola neplatné ceny - měla by být převedena na 0.0
    assert cars[1].get_price() == 0.0

    # Kontrola platného záznamu s platnou cenou
    assert cars[2].model == "Škoda Fabia"
    assert cars[2].get_price() == 300000.0


# Test načítání dat ze souboru XML pomocí XmlDataLoader
def test_xml_data_loader(tmp_path):
    # Vytvoříme dočasný XML soubor s testovacími daty
    data = """<?xml version="1.0" encoding="UTF-8"?>
    <cars>
        <car>
            <model>Škoda Octavia</model>
            <datum>4.12.2020</datum>
            <cena>500000</cena>
        </car>
        <car>
            <model>Škoda Superb</model>
            <datum>5.12.2019</datum>
            <cena>neplatná</cena>
        </car>
        <car>
            <model>Škoda Fabia</model>
            <datum>6.12.2018</datum>
            <cena>300000</cena>
        </car>
    </cars>
    """
    
    file_path = tmp_path / "test_data.xml"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(data)
    
    # Načteme data pomocí XmlDataLoader
    loader = XmlDataLoader()
    cars = loader.load_data(str(file_path))

    # Ověříme, že data byla správně načtena
    assert len(cars) == 3
    assert isinstance(cars[0], Car)
    assert cars[0].model == "Škoda Octavia"
    assert cars[0].sale_date == "2020.12.04"  # Datum je převedeno na formát YYYY.MM.DD
    assert cars[0].price == 500000

    # Kontrola neplatné ceny - měla by být převedena na 0.0
    assert cars[1].get_price() == 0.0

    # Kontrola platného záznamu s platnou cenou
    assert cars[2].model == "Škoda Fabia"
    assert cars[2].get_price() == 300000.0
