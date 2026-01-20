# PostgreSQL
## 1. Fundament Relacyjny: PostgreSQL
Zastosowanie: Dane krytyczne, finanse i spójność.

## 2. Użytkownicy (Profile i Role)
Argumentacja: Dane tożsamościowe wymagają najwyższego poziomu integralności. PostgreSQL pozwala na rygorystyczne wymuszenie unikalności (np. adresów e-mail) oraz budowanie trwałych relacji między użytkownikami a ich uprawnieniami (RBAC). Dzięki temu unikasz duplikacji i błędów w autoryzacji.

## 3. Stany Magazynowe
Argumentacja: To obszar wymagający ścisłej atomowości (ACID). PostgreSQL idealnie radzi sobie z wyścigami (race conditions) – np. gdy wielu użytkowników próbuje kupić ostatnią sztukę towaru w tym samym czasie. Mechanizmy blokad (locking) gwarantują, że stan magazynowy nigdy nie spadnie poniżej zera przez błąd bazy.

## 4. Zamówienia i Płatności
Argumentacja: Dane finansowe muszą być audytowalne i nienaruszalne. Relacyjny model pozwala na precyzyjne rozbicie zamówienia na tabele (nagłówek zamówienia, pozycje, historia statusów), co ułatwia generowanie faktur i raportowanie księgowe, gdzie każdy grosz musi się zgadzać.

## 5. Koszyk
Argumentacja: Przeniesienie koszyka do PostgreSQL (w przeciwieństwie do Ulubionych) sugeruje system, w którym koszyk jest silnie powiązany z aktualną rezerwacją stanów magazynowych lub cennikami. Gwarantuje to, że to, co użytkownik widzi w koszyku, jest bezpośrednio spójne z logiką biznesową zaplecza.

## 6. Kategorie (Struktura i Hierarchia) – PostgreSQL
Argumentacja: Kategorie w e-commerce rzadko są płaską listą; zazwyczaj tworzą złożone drzewo (np. Elektronika > Komputery > Laptopy). PostgreSQL oferuje zaawansowane mechanizmy do obsługi danych hierarchicznych (np. zapytania rekurencyjne WITH RECURSIVE lub typ danych ltree).

# MongoDB
## 1. Elastyczna Warstwa Dokumentowa: MongoDB
Zastosowanie: Skala, dynamika i wydajność odczytu.

## 2. Katalog Produktów z Wariantami
Argumentacja: Produkty w e-commerce to dane heterogeniczne (każda kategoria ma inne cechy). MongoDB stosuje dynamiczny schemat (schema-less), co pozwala uniknąć tzw. "piekła złączeń" lub niewydajnego modelu EAV (Entity-Attribute-Value) w SQL. Nowe parametry produktu dodajesz natychmiast, bez kosztownych migracji bazy.

## 3. Ulubione
Argumentacja: To dane o wysokiej częstotliwości modyfikacji, ale mniejszym znaczeniu krytycznym dla systemu finansowego. MongoDB oferuje ekstremalnie niskie opóźnienia (latency), co sprawia, że interfejs użytkownika reaguje błyskawicznie przy dodawaniu przedmiotów do "wishlisty".

## 4. Recenzje
Argumentacja: Recenzje to obiekty, które świetnie modeluje się jako dokumenty. Można w nich osadzać (embedding) odpowiedzi administracji czy metadane o autorze. Pozwala to na pobranie całej sekcji komentarzy pod produktem za pomocą jednego, szybkiego zapytania do bazy, bez konieczności łączenia wielu tabel.

## 5. Historia Transakcji (Snapshoty)
Argumentacja: To kluczowy zabieg architektoniczny. Podczas gdy PostgreSQL trzyma dane "żywe", MongoDB przechowuje dokumenty historyczne. Zapisujesz tam pełny obraz zamówienia (ceny, opisy, parametry) z momentu zakupu. Nawet jeśli produkt zostanie usunięty z katalogu lub zmieni cenę, historia w MongoDB pozostaje niezmiennym dowodem na to, co dokładnie klient kupił.

# Warstwa aplikacji
## 1. Decydowanie o procesach
Warstwa aplikacji będzie musiała tutaj decydować kiedy użyć PostgreSQL, a kiedy MongoDB. Bazy wówczas będą pilnować poprawności danych.

## 2. Spójność międzybazowa
Aplikacja będzie tu odpowiadać za kolejność operacji (na przykład zapis danych historycznych do MongoDB po złożeniu zamówienia [obsłużonego w PostgreSQL]) oraz za obsługę potencjalnych błędów i na przykład ponawianie operacji.

## 3. Mapowanie modeli domenowych
Mapowanie tabel relacyjnych na encje domenowe i dokumenty MongoDB, ponieważ każda warstwa inaczej reprezentuje dane, z których korzysta.

## 4. Autoryzacja i kontrola dostępu
Typowa rola aplikacji.

## 5. Agregacja danych
Tworzenie spójnego ViewModelu na podstawie połączenia danych z obu baz danych (zależnie od zapytania od użytkownika).

## 6. Walidacja reguł
Typowa rola aplikacji.
