# Zakres Projektu

Zakres projektu obejmuje implementację wszystkich encji i relacji widocznych na diagramie, co sprowadza się do następujących głównych modułów i funkcjonalności:

## 1. Moduł Katalogu Produktów i Wariantów

**Zarządzanie Produktami:**  
- Definiowanie podstawowych informacji o produkcie (`Product`).

**Kategorie i Producenci:**  
- Przypisywanie produktów do kategorii (`Category`) i producentów (`Manufacturer`).

**Obsługa Wariantów:**  
- Modelowanie wariantów produktów (`Variant`) – kluczowy element umożliwiający różnicowanie produktów na podstawie atrybutów (np. rozmiar, kolor).

**Atrybuty Wariantów:**  
- Definiowanie atrybutów (`Attribute`) i ich opcji (`Option`).

## 2. Moduł Użytkowników i Interakcji

**Zarządzanie Kontami:**  
- Rejestracja, uwierzytelnianie i profil użytkownika (`User`).

**Ulubione Produkty:**  
- Funkcjonalność dodawania produktów do listy ulubionych (`FavoriteProduct`).

**Recenzje:**  
- System umożliwiający użytkownikom dodawanie recenzji i ocen do produktów (`Review`).

## 3. Moduł Logistyki i Magazynu

**Zarządzanie Magazynem:**  
- Definicja magazynów i ich lokalizacji (`Warehouse`).

**Stan Magazynowy:**  
- Każdy egzemplarz produktu w magazynie jest ujęty w ewidencji i niezależnie śledzony (`StockItem`).

## 4. Moduł Procesowania Zamówień i Transakcji

**Koszyk Zakupowy:**  
- Mechanizm koszyka (`Cart`) i pozycji w koszyku (`CartItem`), łączący użytkownika z wybranymi wariantami.

**Składanie Zamówień:**  
- Tworzenie zamówienia (`Order`), zawierającego pozycje zamówienia (`OrderItem`), które odnoszą się do konkretnych egzemplarzy produktu w magazynie.

**Metody Płatności i Dostawy:**  
- Zapisywanie informacji o wybranej metodzie płatności (`PaymentMethod`) i dostawy (`DeliveryMethod`).

**Promocje:**  
- Możliwość zastosowania i śledzenia promocji (`Promotion`) powiązanych z zamówieniami.

**Dostawy:**
- Pojedyncze zamówienie (`Order`) może zostać rozdzielone na kilka niezależnych dostaw (przesyłek). Całe zamówienie jest powiązane z jedną metodą dostawy (`DeliveryMethod`).

**Stan Zamówienia:**  
- Zamówienia posiadają różne stany (`Status`).

# Poza Zakresem Projektu

Poniższe elementy nie są reprezentowane bezpośrednio w dostarczonym ERD i stanowią rozszerzenie projektu, które nie zostanie zaimplementowane w ramach obecnego zakresu:

## 1. Ograniczenia Procesów Zamówień i Transakcji

- **Historia Płatności:**  
  System nie będzie śledził historii płatności ani częściowych płatności dla pojedynczego zamówienia. Zamówienie (`Order`) jest powiązane z jedną, finalną metodą płatności (`PaymentMethod`) i zakłada się, że płatność jest przetwarzana jednorazowo.

- **Zwroty i Reklamacje:**  
  Procesowanie zwrotów, wymian, anulowań i refundacji jest poza zakresem.

## 2. Ograniczenia Katalogu i Atrybutów

- **Wielu Producentów:**  
  Dany produkt (`Product`) może pochodzić tylko od jednego producenta (`Manufacturer`). Relacja między nimi jest 1 do 1/N i nie dopuszcza wielu producentów dla tego samego produktu.

- **Zmiany Atrybutów:**  
  System nie śledzi historii zmian atrybutów, cen czy stanów magazynowych w czasie.

## 3. Ograniczenia Promocji (Reguły Biznesowe)

- **Łączenie Promocji:**  
  Promocje się nie łączą. Związek między `Variant` a `Promotion` oznacza, że dany wariant może mieć tylko jedną aktywną promocję w danym zamówieniu, co zapobiega kumulacji rabatów.
