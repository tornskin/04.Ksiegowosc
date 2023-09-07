from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Konfiguracja bazy danych SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)


# Definicja modeli
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    operation = db.Column(db.String(50), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class Manager:
    actions = {}

    def __init__(self):
        self.saldo = 1000.0
        self.history = []
        self.initial_message = "Witaj w aplikacji obsługi magazynu. Lista dostępnych operacji:\n" \
                               " 1. Saldo\n 2. Sprzedaż\n 3. Zakup\n 4. Konto\n 5. Lista\n 6. Magazyn\n 7. Przegląd\n 8. Koniec\n"
        self.end_program = False

    def execute(self, name):
        if name not in self.actions:
            print("Wybacz, nie ma takiej operacji.")
        else:
            self.actions[name](self)

    def start(self):
        while not self.end_program:
            print(self.initial_message)
            operation = input("Wybierz operację wprowadzając odpowiedni numer: ")
            self.execute(operation)


manager = Manager()


@app.route('/')
def index():
    products = Product.query.all()
    saldo = manager.saldo
    return render_template('index.html', products=products, saldo=saldo)


@app.route('/purchase', methods=['POST'])
def purchase():
    product_name = request.form['product']
    price = float(request.form['price'])
    quantity = int(request.form['quantity'])

    product = Product.query.filter_by(name=product_name).first()

    if product:
        product.quantity += quantity
        transaction = Transaction(operation="Zakup", product_id=product.id, quantity=quantity)
    else:
        product = Product(name=product_name, quantity=quantity, price=price)
        transaction = Transaction(operation="Zakup", product=product, quantity=quantity)

    db.session.add(product)
    db.session.add(transaction)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/sale', methods=['POST'])
def sale():
    product_name = request.form['product']
    quantity = int(request.form['quantity'])

    product = Product.query.filter_by(name=product_name).first()

    if product:
        if product.quantity >= quantity:
            product.quantity -= quantity
            transaction = Transaction(operation="Sprzedaż", product_id=product.id, quantity=quantity)
            db.session.add(transaction)
            db.session.commit()
        else:
            manager.history.append(f"Nie udało się sprzedać towaru {product_name}, zbyt mała ilość na magazynie")
            db.session.rollback()

    return redirect(url_for('index'))


@app.route('/change_balance', methods=['POST'])
def change_balance():
    amount_str = request.form['amount']

    # Upewnij się, że wartość jest niepustym łańcuchem
    if not amount_str:
        return redirect(url_for('index'))  # Powrót do strony głównej bez zmiany salda

    try:
        amount = float(amount_str)
    except ValueError:
        return redirect(url_for('index'))  # Powrót do strony głównej w przypadku błędnej wartości

    if amount != 0.0:
        manager.saldo += amount
        # Przypisz stałą wartość product_id do transakcji zmiany salda
        transaction = Transaction(operation="Zmiana Salda", product_id=0, quantity=amount)
        db.session.add(transaction)
        db.session.commit()

    return redirect(url_for('index'))


@app.route('/history', defaults={'start': None, 'end': None})
@app.route('/history/<int:start>/<int:end>')
def history(start, end):
    if start is None and end is None:
        history_data = Transaction.query.all()
    else:
        history_len = len(manager.history)
        if start is None or end is None or start < 1 or end > history_len or start > end:
            return render_template('history_range.html', history_len=history_len)
        history_data = Transaction.query.order_by(Transaction.timestamp).slice(start - 1, end)

    return render_template('history.html', history_data=history_data)


if __name__ == "__main__":
    app.run(debug=True)
