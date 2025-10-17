# Wymagania Funkcjonalne – System E-commerce

## 1. Zarządzanie Użytkownikami i Dostępem

### 1.1 Rejestracja i logowanie

- System umożliwia tworzenie nowych kont użytkowników poprzez formularz rejestracyjny.  
- Logowanie odbywa się na podstawie unikalnego adresu e-mail i hasła.  
- Hasła muszą być przechowywane w sposób zaszyfrowany.  
- System umożliwia mechanizm odzyskiwania hasła.  
- Po zalogowaniu użytkownik otrzymuje token sesyjny/autoryzacyjny.

### 1.2 Role i poziomy dostępu

System definiuje cztery główne poziomy dostępu:

| Rola | Uprawnienia | Przykładowe działania |
|------|--------------|-----------------------|
| **Administrator (Admin)** | Pełny dostęp do systemu. Zarządza użytkownikami, produktami, zamówieniami i promocjami. | Dodawanie nowych użytkowników, edycja ról, usuwanie produktów, zmiana stanów magazynowych. |
| **Redaktor (Editor)** | Zarządzanie katalogiem produktów, producentami, kategoriami, wariantami i promocjami. | Dodawanie/edycja produktów, wprowadzanie promocji, aktualizacja opisów. |
| **Użytkownik (User)** | Składanie zamówień, dodawanie recenzji, korzystanie z koszyka i ulubionych. | Dodanie do koszyka, wystawienie recenzji, składanie zamówienia. |
| **Pracownik Magazynu (Warehouse Operator)** | Dostęp do modułu stanów magazynowych, aktualizacja ilości i lokalizacji. | Wprowadzanie przyjęć i wydań magazynowych, aktualizacja stanów. |
| **Gość (Guest)** | Dostęp do przeglądania katalogu produktów. | Przeglądanie dostępnych produktów. |

**Reguły dostępu:**
- Każdy użytkownik może mieć przypisaną tylko jedną rolę.    
- Uprawnienia określają widoczność oraz możliwość edycji danych w systemie.  

---

## 2. Zarządzanie Katalogiem Produktów

### 2.1 Produkty
- System umożliwia tworzenie, edycję, usuwanie i przeglądanie produktów.  
- Każdy produkt musi należeć przynajmniej do jednej kategorii i musi mieć przypisanego jednego producenta.   
- System umożliwia wyszukiwanie produktów po nazwie, kategorii, producencie i cenie.
- Produkty są powiązane z atrybutami (np. kolor).  

### 2.2 Kategorie i producenci  
- Produkt może być przypisany do wielu kategorii.  
- Producent może posiadać wiele produktów, ale produkt może mieć tylko jednego producenta.  

### 2.3 Warianty produktów
- System umożliwia definiowanie wariantów (np. kolor, rozmiar, pojemność).  
- Każdy wariant posiada własny stan magazynowy w postaci 'StockItem' i może mieć osobną cenę/promocję.  
- Warianty są powiązane z atrybutami i opcjami (np. kolor: czerwony).  

---

## 3. Zarządzanie Zamówieniami i Koszykiem

### 3.1 Koszyk zakupowy
- Każdy zalogowany użytkownik może posiadać jeden aktywny koszyk.
- Koszyk zawiera pozycję 'CartItem', odnoszące się do konkretnego wariantu
- Do koszyka można dodawać i usuwać warianty produktów.  
- System aktualizuje wartość koszyka po każdej zmianie.
- Dostępność wariantu jest weryfikowana w tabeli 'StockItem'.
  
### 3.2 Składanie zamówienia
- Użytkownik może złożyć zamówienie na podstawie zawartości koszyka.  
- System wymaga podania metody płatności i dostawy.  
- Po złożeniu zamówienia generowany jest unikalny numer zamówienia.    
- Zamówienia są przypisane do użytkownika, który je utworzył.  

### 3.3 Płatność i dostawa
- Każde zamówienie jest powiązane z jedną metodą płatności i jedną metodą dostawy.  
- System nie obsługuje wielu płatności dla jednego zamówienia.
- Dla każdej metody dostawy określony jest koszt.
- Płatność i dostawa są wybierane z listy dostępnych opcji.
- Dla jednego zamówienia może być wiele przesyłek.

---

## 4. Promocje i Rabaty
- System umożliwia definiowanie promocji z określonym okresem obowiązywania.  
- Promocja może być przypisana do wariantu.  
- Promocje się nie łączą — dla danego wariantu obowiązuje tylko jedna aktywna promocja.  
- Cena końcowa zamówienia jest obliczana z uwzględnieniem promocji.  

---

## 5. Recenzje i Opinie 
- Każda recenzja zawiera:
  - ocenę (np. 1–5),  
  - treść komentarza.  
- Recenzje są powiązane z użytkownikiem i produktem.  
- Administrator może usuwać recenzje naruszające regulamin.  

---

## 6. Zarządzanie Magazynem, Stanami i Wysyłkami
- System umożliwia definiowanie wielu magazynów.   
- Po utworzeniu wysyłki aktualizowany jest stan magazynowy. 
- Pracownik magazynu może ręcznie zmieniać ilości (np. korekty).
- Każda wysyłka jest powiązana z jednym zamówieniem.

---

## 7. Mechanizmy Wyszukiwania i Filtrowania
System umożliwia m.in.:
- wyszukiwanie produktów według kategorii, producenta, ceny i promocji,  
- wyświetlanie historii zamówień użytkownika,  
- sprawdzanie stanów magazynowych dla wariantów,  
- analizę sprzedaży (np. najczęściej sprzedawane produkty),  
- pobranie średniej oceny produktu na podstawie recenzji.  
