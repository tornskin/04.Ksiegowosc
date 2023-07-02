'''Napisz program, który będzie rejestrował operacje na koncie firmy i stan magazynu.

Program po uruchomieniu wyświetla informację o dostępnych komendach:

saldo
 sprzedaż
zakup
konto
lista
magazyn
przegląd
koniec

Po wprowadzeniu odpowiedniej komendy, aplikacja zachowuje się w unikalny sposób dla każdej z nich:

saldo - Program pobiera kwotę do dodania lub odjęcia z konta.
sprzedaż - Program pobiera nazwę produktu, cenę oraz liczbę sztuk. Produkt musi znajdować się w magazynie. Obliczenia respektuje względem konta i magazynu (np. produkt "rower" o cenie 100 i jednej sztuce spowoduje odjęcie z magazynu produktu "rower" oraz dodanie do konta kwoty 100).
zakup - Program pobiera nazwę produktu, cenę oraz liczbę sztuk. Produkt zostaje dodany do magazynu, jeśli go nie było. Obliczenia są wykonane odwrotnie do komendy "sprzedaz". Saldo konta po zakończeniu operacji „zakup” nie może być ujemne.
konto - Program wyświetla stan konta.
lista - Program wyświetla całkowity stan magazynu wraz z cenami produktów i ich ilością.
magazyn - Program wyświetla stan magazynu dla konkretnego produktu. Należy podać jego nazwę.
przegląd - Program pobiera dwie zmienne „od” i „do”, na ich podstawie wyświetla wszystkie wprowadzone akcje zapisane pod indeksami od „od” do „do”. Jeżeli użytkownik podał pustą wartość „od” lub „do”, program powinien wypisać przegląd od początku lub/i do końca. Jeżeli użytkownik podał zmienne spoza zakresu, program powinien o tym poinformować i wyświetlić liczbę zapisanych komend (żeby pozwolić użytkownikowi wybrać odpowiedni zakres).
koniec - Aplikacja kończy działanie.

Dodatkowe wymagania:

Aplikacja od uruchomienia działa tak długo, aż podamy komendę "koniec".
Komendy saldo, sprzedaż i zakup są zapamiętywane przez program, aby móc użyć komendy "przeglad".
Po wykonaniu dowolnej komendy (np. "saldo") aplikacja ponownie wyświetla informację o dostępnych komendach, a także prosi o wprowadzenie jednej z nich.
Zadbaj o błędy, które mogą się pojawić w trakcie wykonywania operacji (np. przy komendzie "zakup" jeśli dla produktu podamy ujemną kwotę, aplikacja powinna wyświetlić informację o niemożności wykonania operacji i jej nie wykonać). Zadbaj też o prawidłowe typy danych.
'''
saldo = 1000.0
warehouse = {
    "bułka": {
        "ilość": 10,
        "cena": 2
    },
    "bagietka": {
        "ilość": 5,
        "cena": 3
    }
}
history = []
initial_message = "Witaj w aplikacji obsługi magazynu. Lista dostępnych operacji:\n" \
    " 1. Saldo\n 2. Sprzedaż\n 3. Zakup\n 4. Konto\n 5. Lista\n 6. Magazyn\n 7. Przegląd\n 8. Koniec\n"

def save_data():
    with open("data.txt", "w") as file:
        file.write(str(saldo) + "\n")
        file.write(str(warehouse) + "\n")
        file.write("\n".join(history))

def load_data():
    global saldo, warehouse, history
    try:
        with open("data.txt", "r") as file:
            saldo = float(file.readline().strip())
            warehouse = eval(file.readline().strip())
            history = file.read().splitlines()
    except FileNotFoundError:
        print("Nie znaleziono pliku z danymi. Tworzenie nowego pliku.")

load_data()

end_program = False
while not end_program:
    print(initial_message)
    operation = input("Wybierz komendę poprzez wpisanie odpowiedniego numeru: ")
    match operation:
        case    "1":
            option = (input("Podaj rodzaj operacji:\n 1. Powiększenie salda\n 2. Pomniejszenie salda\n"))
            if option == "1":
                amount = float(input("Podaj kwotę: "))
                if amount > 0:
                    saldo += amount
                    history.append(f"Zmieniono saldo o kwotę: {amount}") #added history
                else:
                    print("Podana wartość nie jest dodatnia.")
            elif option == "2":
                amount = float(input("Podaj kwotę: "))
                if amount < 0:
                    saldo += amount
                    history.append(f"Zmieniono saldo o kwotę: {amount}") #added history
                else:
                    print("Podana wartość nie jest ujemna.")
            else:
                print("Wybrano niepoprawny numer operacji.")

            print(saldo)

        case "2":
            print(warehouse)
            try:
                product, amount = tuple(
                    input("Podaj nazwę produktu i ilość po przecinku: ").replace(" ", "").split(","))
                amount = int(amount)
                product_found = False
                insufficient_quantity = False
                for item, item_details in warehouse.items():
                    if product == item:
                        product_found = True
                        if item_details["ilość"] >= amount:
                            item_details["ilość"] -= amount
                            saldo += item_details["cena"] * amount
                            history.append(f"Sprzedano {product} w ilości {amount}") ##added history
                        else:
                            insufficient_quantity = True
                        break

                if not product_found:
                    print("Nie znaleziono takiego produktu.")
                elif insufficient_quantity:
                    print(f'Brak towaru w takiej ilości. Liczba dostępnych sztuk to: {item_details["ilość"]}.')
                    history.append(f"Nie udało się sprzedać towaru {product}, zbyt mała ilość na magazynie")  ##added history

            except ValueError:
                print("Niepoprawny format, poprawny zapis to: produkt,ilość")

        case "3":
            try:
                product, amount = tuple(
                    input("Podaj nazwę produktu, który chcesz zakupić i jego ilość po przecinku: ").replace(" ",
                                                                                                            "").split(
                        ","))
                amount = int(amount)
                product_found = False

                for item, item_details in warehouse.items():
                    if product == item:
                        product_found = True
                        if saldo < item_details["cena"] * amount:
                            print("Brak wystarczających środków na zakup.")
                            break
                        item_details["ilość"] += amount
                        saldo -= item_details["cena"] * amount
                        history.append(f"Zakupiono {product} w ilości {amount}")  ##added history
                        break

                if not product_found:
                    price = float(input("Podaj cenę produktu: "))
                    warehouse[product] = {
                        "ilość": amount,
                        "cena": price
                    }
                    saldo -= price * amount
                    history.append(f"Dodano nowy produkt: {product} w ilości {amount} po cenie {price}")

            except ValueError:
                print("Niepoprawny format, poprawny zapis to: produkt,ilość")

        case "4":
            print(f"Aktualny stan konta: {saldo}")

        case "5":
            print(warehouse)

        case "6":
            product = input("Podaj nazwę towaru, którego stan chcesz sprawdzić: ")
            product_found = False
            for item, item_details in warehouse.items():
                if product == item:
                    product_found = True
                    print(item_details)
                    break
            if not product_found:
                print("Nie znaleziono takiego produktu w magazynie.")

        case "7":
            while True:
                value_from = input("Podaj początkowy zakres: ")
                value_to = input("Podaj końcowy zakres: ")

                if value_to > "3":
                    print("Zakres końcowy nie może być większy niż 3.")
                    continue
                if not value_to and not value_to:
                    print(history)
                    break
                if value_from and not value_to:
                    value_from = int(value_from) - 1
                    print(history[value_from:])
                    break
                if not value_from and value_to:
                    value_to = int(value_to)
                    print(history[:value_to])
                    break
                if value_from and value_to:
                    value_from = int(value_from) - 1
                    value_to = int(value_to)
                    print(history[value_from:value_to])
                    break
        case "8":
            end_program = True
            save_data()
        case other:
            print("Nieprawidłowa komenda, wprowadź numer ponownie.\n")