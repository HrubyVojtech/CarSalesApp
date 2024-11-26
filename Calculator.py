class Calculator:
    def __init__(self, ui):
        self.ui = ui

    def calculate_total(self, cars):
        year = self.ui.year_input.currentText()
        if not year.isdigit():
            self.ui.total_label.setText("Prosím, zadejte platný rok.")
            return
        
        selected_model = self.ui.model_filter.currentText()
        total = 0

        for car in cars:
            if car.sale_date.startswith(year) and (selected_model == "Všechny modely" or car.model == selected_model):
                total += car.get_price()

        total_with_vat = total * 1.21
        self.ui.total_label.setText(f'Celková cena s DPH: {total_with_vat:,.2f} Kč')

    