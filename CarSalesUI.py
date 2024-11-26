from PyQt5.QtWidgets import QVBoxLayout, QWidget, QPushButton, QTableWidget, QComboBox, QLabel, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt

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
