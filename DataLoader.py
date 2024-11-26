from PyQt5.QtWidgets import QFileDialog
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from Car import Car

class DataLoader:
    def load_data(self, file_name):
        raise NotImplementedError("Must override load_data method")

class JsonDataLoader(DataLoader):
    def load_data(self, file_name):
        cars = []
        with open(file_name, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for item in data:
                try:
                    sale_date = datetime.strptime(item['Datum prodeje'], "%d.%m.%Y").strftime("%Y.%m.%d")
                except ValueError:
                    sale_date = None
                car = Car(item['Název modelu'], sale_date, item['Cena bez DPH'])
                cars.append(car)
        return cars
    
class XmlDataLoader(DataLoader):
    def load_data(self, file_name):
        cars = []
        try:
            tree = ET.parse(file_name)
            root = tree.getroot()
            rows = root.findall('car')
            for car_element in rows:
                model = car_element.find('model').text if car_element.find('model') is not None else ""
                sale_date = car_element.find('datum').text if car_element.find('datum') is not None else ""
                try:
                    sale_date = datetime.strptime(sale_date, "%d.%m.%Y").strftime("%Y.%m.%d")
                except ValueError:
                    sale_date = ""
                price = car_element.find('cena').text if car_element.find('cena') is not None else ""
                car = Car(model, sale_date, price)
                cars.append(car)
        except ET.ParseError:
            pass
        return cars

class FileLoader:
    def __init__(self, ui):
        self.ui = ui

    def load_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self.ui.main_window, "Načíst soubor", "", "JSON Files (*.json);;XML Files (*.xml);;All Files (*)", options=options)
        if not file_name:
            return

        if file_name.endswith('.json'):
            loader = JsonDataLoader()
        elif file_name.endswith('.xml'):
            loader = XmlDataLoader()
        else:
            return

        cars = loader.load_data(file_name)

        self.ui.update_cars(cars, file_name)