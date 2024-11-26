from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QTableWidget, QTableWidgetItem, QLineEdit, QLabel, QComboBox, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
import sys
from CarSalesUI import CarSalesUI
from datetime import datetime
from DataLoader import FileLoader
from Calculator import Calculator




class CarSalesApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cars = []
        self.max_price = 0

        # Iniciace tříd
        self.ui = CarSalesUI(self)
        self.calculator = Calculator(self.ui)
        self.file_loader = FileLoader(self.ui)



        # Propojení signálů
        self.ui.load_button.clicked.connect(self.file_loader.load_file)
        self.ui.model_filter.currentIndexChanged.connect(self.filter_table_by_model)
        self.ui.calculate_button.clicked.connect(lambda: self.calculator.calculate_total(self.cars))
        self.ui.table.horizontalHeader().sectionClicked.connect(self.sort_table)
        self.ui.year_input.currentTextChanged.connect(self.year_changed)

   
    def update_table(self): # Metoda pro aktualizaci tabulky
        self.ui.table.setRowCount(0)  # Clear previous data
        self.ui.table.setRowCount(len(self.cars))
        self.ui.table.setColumnCount(3)
        self.ui.table.setHorizontalHeaderLabels(["Název modelu", "Datum prodeje", "Cena bez DPH"])

        models = set()  # Použijeme množinu, abychom zajistili unikátní modely

        for row, car in enumerate(self.cars):
            model_item = QTableWidgetItem(car.model)
            date_item = QTableWidgetItem(car.sale_date)
            price_item = QTableWidgetItem(str(car.price))

            # Uložení dat pro správné třídění
            if car.sale_date:
                try:
                    date_item.setData(Qt.UserRole, datetime.strptime(car.sale_date, "%Y.%m.%d"))
                except ValueError:
                    date_item.setData(Qt.UserRole, None)  # Pokud je špatný formát datumu

            price_item.setData(Qt.EditRole, car.get_price())

            self.ui.table.setItem(row, 0, model_item)
            self.ui.table.setItem(row, 1, date_item)
            self.ui.table.setItem(row, 2, price_item)

            models.add(car.model)

        # Naplnění výběrového pole modelů
        self.ui.model_filter.clear()
        self.ui.model_filter.addItem("Všechny modely")
        for model in sorted(models):
            self.ui.model_filter.addItem(model)

    def update_year_options(self): # Metoda pro aktualizaci možností výběrového pole s roky
        years = set()
        for car in self.cars:
            if car.sale_date:
                try:
                    year = datetime.strptime(car.sale_date, "%Y.%m.%d").year
                    years.add(str(year))
                except ValueError:
                    continue
        
        self.ui.year_input.clear()
        self.ui.year_input.addItem("")  # Prázdná možnost
        self.ui.year_input.addItems(sorted(years))

    def update_max_price(self): # Metoda pro aktualizaci maximální ceny
        self.max_price = max((car.get_price() for car in self.cars), default=0)

    def apply_price_backgrounds(self): # Nastavení barvy pozadí pro hodnoty ceny podle výše ceny
        for row in range(self.ui.table.rowCount()):
            price_item = self.ui.table.item(row, 2)
            if price_item:
                try:
                    price_value = float(price_item.text().replace(',', '').replace(' ', ''))
                    if self.max_price > 0:
                        alpha_intensity = int(255 * (price_value / self.max_price))
                        alpha_intensity = max(50, min(alpha_intensity, 255))  # Zajištění, že hodnota je v rozsahu 50-255
                        price_item.setBackground(QtGui.QColor(0, 255, 0, alpha_intensity))  # Nastavení barvy pozadí (různé stupně průhlednosti zelené)
                except ValueError:
                    pass

    def filter_table_by_model(self): # Metoda pro filtrování tabulky podle modelu
        selected_model = self.ui.model_filter.currentText()

        
        for row in range(self.ui.table.rowCount()):
            item = self.ui.table.item(row, 0)  # První sloupec obsahuje modely
            if item:
                if selected_model == "Všechny modely" or item.text() == selected_model:
                    self.ui.table.setRowHidden(row, False)
                else:
                    self.ui.table.setRowHidden(row, True)

   
    def sort_table(self, index):
        pass

    def year_changed(self):
        pass

   
if __name__ == '__main__': # Spuštění aplikace
    app = QApplication(sys.argv)
    main_window = CarSalesApp()
    main_window.show()
    sys.exit(app.exec_())
