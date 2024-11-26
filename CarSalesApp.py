from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtCore import Qt
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

   
    def update_table(self): # Metoda pro aktualizaci tabulky
        self.ui.update_table(self.cars)

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

    def filter_table_by_model(self): # Metoda pro filtrování tabulky podle modelu
        selected_model = self.ui.model_filter.currentText()

        
        for row in range(self.ui.table.rowCount()):
            item = self.ui.table.item(row, 0)  # První sloupec obsahuje modely
            if item:
                if selected_model == "Všechny modely" or item.text() == selected_model:
                    self.ui.table.setRowHidden(row, False)
                else:
                    self.ui.table.setRowHidden(row, True)

   


   
if __name__ == '__main__': # Spuštění aplikace
    app = QApplication(sys.argv)
    main_window = CarSalesApp()
    main_window.show()
    sys.exit(app.exec_())
