
# Car Sales Application

## Overview

This is a Python-based GUI application for managing car sales data. It allows users to load car sales data from JSON or XML files, filter by car models or years, and calculate the total sales including VAT (Value-Added Tax). The application is built using PyQt5, providing a user-friendly interface for interacting with the car sales data.

## Features

- **Data Loading**: Load car sales data from JSON or XML files.
- **Filtering**: Filter car sales data by car model or sales year.
- **Sales Calculation**: Calculate the total sales price including VAT (21%).
- **Interactive GUI**: The application has an intuitive graphical user interface built with PyQt5, which allows easy data interaction, filtering, and calculation.

## Project Structure

- **CarSalesApp.py**: Main application file containing the `CarSalesApp` class, which integrates the user interface and functionalities.
- **CarSalesUI.py**: Defines the user interface elements using PyQt5 components.
- **Calculator.py**: Contains the `Calculator` class responsible for calculating the total price of cars including VAT.
- **Car.py**: Defines the `Car` class, representing individual car records with attributes like model, sale date, and price.
- **DataLoader.py**: Provides functionality for loading car data from JSON and XML files. Includes `JsonDataLoader` and `XmlDataLoader` classes.
- **test_car.py**: Unit tests for the `Car` class to ensure proper initialization and price handling.
- **car_sales.json** and **car_sales.xml**: Example data files containing car sales records.

## Requirements

- Python 3.8 or higher
- PyQt5
- pytest (for running tests)

## Installation

1. **Clone the Repository**:
   ```sh
   git clone <repository-url>
   ```
2. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt
   ```
   *(Ensure **`PyQt5`** is included in your **`requirements.txt`** file or install it manually)*

## Usage

1. **Run the Application**:
   ```sh
   python CarSalesApp.py
   ```
2. **Load Car Data**: Click on "Načíst soubor" to load a car sales file (either JSON or XML).
3. **Filter and Calculate**:
   - Use the dropdown filters to select a specific car model or year.
   - Click on "Vypočítat celkovou cenu s DPH" to calculate the total price including VAT.

## Running Tests

To run unit tests for the `Car` class, use:

```sh
pytest test_car.py
```

## Files Description

- **car_sales.json**: Sample JSON file containing car sales data for testing.
- **car_sales.xml**: Sample XML file containing car sales data for testing.

## Key Classes

- **CarSalesApp**: Manages the main application flow.
- **CarSalesUI**: Handles the user interface layout and components.
- **Calculator**: Performs calculations for total sales with VAT.
- **DataLoader**: Abstract class for loading data, extended by `JsonDataLoader` and `XmlDataLoader`.
- **Car**: Represents a car record with details like model, sale date, and price.

## Future Improvements

- **Database Integration**: Store car sales data in a database for better data management and retrieval.
- **Enhanced Filtering**: Add more filter options, such as price range and sale date.
- **Data Visualization**: Include charts to visualize sales data trends over time.

## License

This project is licensed under the MIT License.

## Author

Developed by Vojtěch Hrubý. Feel free to contribute or report issues to improve the project. If you have suggestions or want to collaborate, don't hesitate to reach out.
