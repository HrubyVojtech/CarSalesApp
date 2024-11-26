from PyQt5.QtWidgets import QVBoxLayout, QWidget, QPushButton, QTableWidget, QComboBox, QLabel, QHBoxLayout, QSizePolicy, QTableWidgetItem
from PyQt5.QtCore import Qt
from datetime import datetime
from PyQt5 import QtGui


class CarSalesUI:
    def __init__(self, main_window):
        self.main_window = main_window
        self.main_window.setGeometry(450, 100, 600, 700)  # Nastavuje velikost na 600x700 pixelů
        self.central_widget = QWidget(main_window)
        self.main_layout = QVBoxLayout()
        
        # Load file button
        self.load_button = QPushButton('Načíst soubor', main_window)
        self.main_layout.addWidget(self.load_button)

        # Filter Layout
        filter_layout = QHBoxLayout()
        self.model_filter = QComboBox(main_window)
        self.model_filter.addItem("Všechny modely")
        self.model_filter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        filter_layout.addWidget(QLabel("Filtr modelu: "))
        filter_layout.addWidget(self.model_filter)
        self.main_layout.addLayout(filter_layout)

        # Year Input Layout
        year_layout = QHBoxLayout()
        self.year_input = QComboBox(main_window)
        self.year_input.setEditable(True)
        self.year_input.lineEdit().setPlaceholderText("Zadejte rok")
        self.year_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        year_layout.addWidget(QLabel("Rok: "))
        year_layout.addWidget(self.year_input)
        self.main_layout.addLayout(year_layout)

        # Table widget
        self.table = QTableWidget(main_window)
        self.table.setSortingEnabled(True)
        self.main_layout.addWidget(self.table)


        # Calculate Button
        self.calculate_button = QPushButton('Vypočítat celkovou cenu s DPH', main_window)
        self.main_layout.addWidget(self.calculate_button)

        # Total Label
        self.total_label = QLabel('Celková cena s DPH: ', main_window)
        self.total_label.setStyleSheet("font-weight: bold; font-size: 18px;")
        self.main_layout.addWidget(self.total_label)

        # Set layout
        self.central_widget.setLayout(self.main_layout)
        main_window.setCentralWidget(self.central_widget)


    def update_table(self, cars): # Metoda pro aktualizaci tabulky
        self.table.setRowCount(0)  # Clear previous data
        self.table.setRowCount(len(cars))
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Název modelu", "Datum prodeje", "Cena bez DPH"])

        models = set()  # Použijeme množinu, abychom zajistili unikátní modely

        for row, car in enumerate(cars):
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

            self.table.setItem(row, 0, model_item)
            self.table.setItem(row, 1, date_item)
            self.table.setItem(row, 2, price_item)

            models.add(car.model)

        # Naplnění výběrového pole modelů
        self.model_filter.clear()
        self.model_filter.addItem("Všechny modely")
        for model in sorted(models):
            self.model_filter.addItem(model)

    def update_cars(self, cars, file_name): 
        self.main_window.cars = cars
        self.main_window.update_table()
        self.update_max_price(cars)
        self.apply_price_backgrounds()
        self.main_window.update_year_options()
        self.total_label.setText(f'Načtený soubor: {file_name}')

    def apply_price_backgrounds(self): # Nastavení barvy pozadí pro hodnoty ceny podle výše ceny
        for row in range(self.table.rowCount()):
            price_item = self.table.item(row, 2)
            if price_item:
                try:
                    price_value = float(price_item.text().replace(',', '').replace(' ', ''))
                    if self.max_price > 0:
                        alpha_intensity = int(255 * (price_value / self.max_price))
                        alpha_intensity = max(50, min(alpha_intensity, 255))  # Zajištění, že hodnota je v rozsahu 50-255
                        price_item.setBackground(QtGui.QColor(0, 255, 0, alpha_intensity))  # Nastavení barvy pozadí (různé stupně průhlednosti zelené)
                except ValueError:
                    pass

    def update_max_price(self, cars): # Metoda pro aktualizaci maximální ceny

        self.max_price = max((car.get_price() for car in cars), default=0)