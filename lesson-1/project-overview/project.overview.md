# Streszczenie – Zarys Wymagań Projektu E-commerce

Projekt dotyczy bazy danych dla platformy e-commerce (sklepu internetowego), koncentrującej się na zarządzaniu produktami, zamówieniami, użytkownikami oraz związanymi z nimi procesami, takimi jak recenzje, koszyki i stany magazynowe.

---

## Podstawowe Funkcjonalności

### Zarządzanie Użytkownikami i Kontami
- Rejestracja i logowanie użytkowników.

### Katalog Produktów
- Definiowanie produktów, ich kategorii, producentów i atrybutów/wariantów.

### Obsługa Wariantów Produktów
- Umożliwienie, aby jeden produkt miał wiele wariantów (np. różne rozmiary, kolory), z możliwością śledzenia egzemplarzy w magazynach.

### Proces Zakupowy
- Obsługa koszyka zakupowego, dodawania do ulubionych.

### Realizacja Zamówień
- Proces składania zamówienia, uwzględniający metody dostawy, płatności oraz promocje.

### Zarządzanie Magazynem i Zapasy
- Śledzenie dostępnych egzemplarzy w różnych magazynach.

### Recenzje Produktów
- Umożliwienie użytkownikom oceniania i recenzowania produktów.

---

## Potrzeby Informacyjne

| Obszar | Kluczowe Dane |
|--------|---------------|
| **Użytkownicy i Relacje** | Dane osobowe i kontaktowe klienta, historia zamówień, ulubione produkty, wystawione recenzje, aktualny koszyk. |
| **Katalog Produktów** | Nazwa, opis, producent, kategoria, atrybuty (np. materiał), dostępne egzemplarze danego wariantu. |
| **Cennik/Promocje** | Cena podstawowa produktu/wariantów, szczegóły i okresy obowiązywania promocji. |
| **Logistyka/Zapasy** | Bieżący stan magazynowy każdego wariantu produktu, lokalizacja magazynowa (Warehouse), szczegóły dostaw. |
| **Transakcje/Finanse** | Szczegóły zamówienia (zamówione warianty, ilości), zastosowane metody płatności i dostawy, koszty, dane rozliczeniowe, szczegóły promocji. |
| **Informacje Zwrotne** | Treść i ocena recenzji, powiązanie recenzji z użytkownikiem i produktem. |

---

## Czynności Wyszukiwania
**Za pomocą projektowanej bazy danych można wykonać następujące typowe zapytania:**

### Pytania Dotyczące Produktów i Kategorii
- Jakie produkty należą do danej kategorii i są wyprodukowane przez denego producenta?  
- Jakie warianty są dostępne dla danego produktu (np. kolor, rozmiar pamięci)?  
- Jaki jest bieżący stan magazynowy danego wariantu w danym magazynie?  
- Jakie atrybuty (np. rozmiar, kolor) można przypisać do wariantów dla danego produktu?  
- Które produkty mają obecnie aktywną promocję?  

### Pytania Dotyczące Użytkowników i Recenzji
- Jakie produkty znajdują się aktualnie w koszyku użytkownika o danym ID?  
- Jakie produkty dany użytkownik dodał do listy ulubionych?  
- Jaka jest średnia ocena recenzji dla danego produktu?  
- Jakie recenzje wystawił użytkownik o danym ID?  
- Jaka jest pełna historia zamówień danego użytkownika?  

### Pytania Dotyczące Zamówień i Transakcji
- Jakie pozycje (warianty, ilości) zostały zamówione w zamówieniu o danym numerze?  
- Jaka była zastosowana metoda płatności i dostawy dla danego zamówienia?  
- Jaka promocja została zastosowana do zamówienia, a co za tym idzie, jaka była faktyczna cena końcowa?  
- Które warianty produktów zostały najczęściej sprzedane w ostatnim miesiącu?  
- Ile zamówień zostało złożonych z wykorzystaniem danej metody dostawy w danym okresie?  
