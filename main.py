def assign(name):
    def wrapper(function):
        Manager.actions[name] = function
        return function
    return wrapper

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

@assign("1")
def operation_1(manager):
    option = input("Podaj rodzaj operacji:\n 1. Powiększenie salda\n 2. Pomniejszenie salda\n")
    if option == "1":
        amount = float(input("Podaj kwotę: "))
        if amount > 0:
            manager.saldo += amount
            manager.history.append(f"Zmieniono saldo o kwotę: {amount}")
        else:
            print("Podana wartość nie jest dodatnia.")
    elif option == "2":
        amount = float(input("Podaj kwotę: "))
        if amount < 0:
            manager.saldo += amount
            manager.history.append(f"Zmieniono saldo o kwotę: {amount}")
        else:
            print("Podana wartość nie jest ujemna.")
    else:
        print("Wybrano niepoprawny numer operacji.")
    print(manager.saldo)

@assign("2")
def operation_2(manager):
    print(manager.warehouse)
    try:
        product, amount = tuple(input("Podaj nazwę produktu i ilość po przecinku: ").replace(" ", "").split(","))
        amount = int(amount)
        product_found = False
        insufficient_quantity = False
        for item, item_details in manager.warehouse.items():
            if product == item:
                product_found = True
                if item_details["ilość"] >= amount:
                    item_details["ilość"] -= amount
                    manager.saldo += item_details["cena"] * amount
                    manager.history.append(f"Sprzedano {product} w ilości {amount}")
                else:
                    insufficient_quantity = True
                break

        if not product_found:
            print("Nie znaleziono takiego produktu.")
        elif insufficient_quantity:
            print(f'Brak towaru w takiej ilości. Liczba dostępnych sztuk to: {item_details["ilość"]}.')
            manager.history.append(f"Nie udało się sprzedać towaru {product}, zbyt mała ilość na magazynie")

    except ValueError:
        print("Niepoprawny format, poprawny zapis to: produkt,ilość")

@assign("3")
def operation_3(manager):
    try:
        product, amount = tuple(
            input("Podaj nazwę produktu, który chcesz zakupić i jego ilość po przecinku: ").replace(" ",
                                                                                                     "").split(
                ","))
        amount = int(amount)
        product_found = False

        for item, item_details in manager.warehouse.items():
            if product == item:
                product_found = True
                if manager.saldo < item_details["cena"] * amount:
                    print("Brak wystarczających środków na zakup.")
                    break
                item_details["ilość"] += amount
                manager.saldo -= item_details["cena"] * amount
                manager.history.append(f"Zakupiono {product} w ilości {amount}")
                break

        if not product_found:
            price = float(input("Podaj cenę produktu: "))
            manager.warehouse[product] = {
                "ilość": amount,
                "cena": price
            }
            manager.saldo -= price * amount
            manager.history.append(f"Dodano nowy produkt: {product} w ilości {amount} po cenie {price}")

    except ValueError:
        print("Niepoprawny format, poprawny zapis to: produkt,ilość")

@assign("4")
def operation_4(manager):
    print(f"Aktualny stan konta: {manager.saldo}")

@assign("5")
def operation_5(manager):
    print(manager.warehouse)

@assign("6")
def operation_6(manager):
    product = input("Podaj nazwę towaru, którego stan chcesz sprawdzić: ")
    product_found = False
    for item, item_details in manager.warehouse.items():
        if product == item:
            product_found = True
            print(item_details)
            break
    if not product_found:
        print("Nie znaleziono takiego produktu w magazynie.")

@assign("7")
def operation_7(manager):
    while True:
        value_from = input("Podaj początkowy zakres: ")
        value_to = input("Podaj końcowy zakres: ")

        if value_to > "3":
            print("Zakres końcowy nie może być większy niż 3.")
            continue
        if not value_to and not value_to:
            print(manager.history)
            break
        if value_from and not value_to:
            value_from = int(value_from) - 1
            print(manager.history[value_from:])
            break
        if not value_from and value_to:
            value_to = int(value_to)
            print(manager.history[:value_to])
            break
        if value_from and value_to:
            value_from = int(value_from) - 1
            value_to = int(value_to)
            print(manager.history[value_from:value_to])
            break

@assign("8")
def operation_8(manager):
    manager.end_program = True
    manager.save_data()


if __name__ == "__main__":
    manager = Manager()
    manager.start()