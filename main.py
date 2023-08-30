from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


class Manager:
    actions = {}  # Declaration of the actions dictionary

    def __init__(self):
        self.saldo = 1000.0
        self.warehouse = {
            "bułka": {
                "ilość": 10,
                "cena": 2
            },
            "bagietka": {
                "ilość": 5,
                "cena": 3
            }
        }
        self.history = []
        self.initial_message = "Witaj w aplikacji obsługi magazynu. Lista dostępnych operacji:\n" \
             " 1. Saldo\n 2. Sprzedaż\n 3. Zakup\n 4. Konto\n 5. Lista\n 6. Magazyn\n 7. Przegląd\n 8. Koniec\n"
        self.end_program = False

        self.load_data()

    def save_data(self):
        with open("data.txt", "w") as file:
            file.write(str(self.saldo) + "\n")
            file.write(str(self.warehouse) + "\n")
            file.write("\n".join(self.history))

    def load_data(self):
        try:
            with open("data.txt", "r") as file:
                self.saldo = float(file.readline().strip())
                self.warehouse = eval(file.readline().strip())
                self.history = file.read().splitlines()
        except FileNotFoundError:
            print("Plik nie został znaleziony. Tworzenie nowego pliku.")

    def execute(self, name):
        if name not in self.actions:
            print("Wybacz, nie ma takiej operacji.")
        else:
            self.actions[name](self)

    def start(self):
        self.load_data()
        while not self.end_program:
            print(self.initial_message)
            operation = input("Wybierz operację wprowadzając odpowiedni numer: ")
            self.execute(operation)

manager = Manager()


@app.route('/')
def index():
    return render_template('index.html', saldo=manager.saldo, warehouse=manager.warehouse)


@app.route('/purchase', methods=['POST'])
def purchase():
    product = request.form['product']
    price = float(request.form['price'])
    quantity = int(request.form['quantity'])

    if product in manager.warehouse:
        manager.warehouse[product]['ilość'] += quantity
        manager.saldo -= price * quantity
        manager.history.append(f"Zakupiono {product} w ilości {quantity}")
    else:
        manager.warehouse[product] = {"ilość": quantity, "cena": price}
        manager.saldo -= price * quantity
        manager.history.append(f"Dodano nowy produkt: {product} w ilości {quantity} po cenie {price}")

    manager.save_data()
    return redirect(url_for('index'))


@app.route('/sale', methods=['POST'])
def sale():
    product = request.form['product']
    quantity = int(request.form['quantity'])

    if product in manager.warehouse:
        if manager.warehouse[product]['ilość'] >= quantity:
            manager.warehouse[product]['ilość'] -= quantity
            manager.saldo += manager.warehouse[product]['cena'] * quantity
            manager.history.append(f"Sprzedano {product} w ilości {quantity}")
        else:
            manager.history.append(f"Nie udało się sprzedać towaru {product}, zbyt mała ilość na magazynie")

    manager.save_data()
    return redirect(url_for('index'))


@app.route('/change_balance', methods=['POST'])
def change_balance():
    amount = float(request.form['amount'])
    manager.saldo += amount
    manager.history.append(f"Zmieniono saldo o kwotę: {amount}")
    manager.save_data()
    return redirect(url_for('index'))


@app.route('/history', defaults={'start': None, 'end': None})
@app.route('/history/<int:start>/<int:end>')
def history(start, end):
    if start is None and end is None:
        history_data = manager.history
    else:
        history_len = len(manager.history)
        if start is None or end is None or start < 1 or end > history_len or start > end:
            return render_template('history_range.html', history_len=history_len)
        history_data = manager.history[start - 1:end]  # Poprawione wyodrębnianie podzakresu historii

    return render_template('history.html', history_data=history_data)



if __name__ == "__main__":
    app.run(debug=True)
