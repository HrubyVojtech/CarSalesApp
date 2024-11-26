class Car:
    def __init__(self, model, sale_date, price):
        self.model = model
        self.sale_date = sale_date
        self.price = price

    def get_price(self):
        try:
            return float(self.price)
        except ValueError:
            return 0.0
