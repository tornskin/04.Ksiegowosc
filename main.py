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

initial_message = "Witaj w aplikacji obsługi magazynu. Lista dostępnych operacji:\n" \
    " 1. Saldo\n 2. Sprzedaż\n 3. Zakup\n 4. Konto\n 5. Lista\n 6. Magazyn\n 7. Przegląd\n 8. Koniec\n"

end_program = False
while not end_program:
    print(warehouse)
    print(saldo)
    print(initial_message)
    operation = input("Wybierz komendę poprzez wpisanie odpowiedniego numeru: ")
    match operation:
        case    "1":
            option = (input("Podaj rodzaj operacji:\n 1. Powiększenie salda\n 2. Pomniejszenie salda\n"))
            if option == "1":
                amount = float(input("Podaj kwotę: "))
                if amount > 0:
                    saldo += amount
                else:
                    print("Podana wartość nie jest dodatnia.")
            elif option == "2":
                amount = float(input("Podaj kwotę: "))
                if amount < 0:
                    saldo += amount
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
                        else:
                            insufficient_quantity = True
                        break

                if not product_found:
                    print("Nie znaleziono takiego produktu.")
                elif insufficient_quantity:
                    print(f'Brak towaru w takiej ilości. Liczba dostępnych sztuk to: {item_details["ilość"]}.')

            except ValueError:
                print("Niepoprawny format, poprawny zapis to: produkt,ilość")

        case other:
            print("Nieprawidłowa komenda, wprowadź numer ponownie.\n")