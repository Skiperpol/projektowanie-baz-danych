# Analiza porównawcza projektów w technologii relacyjnej i NoSQL

## 1.  Jakie są główne różnice w projektach zrealizowanych za pomocą bazy relacyjnej i nierelacyjnej?

### 1.1. Normalizacja danych
Dane w projekcie bazy relacyjnej były silnie znormalizowane i zawarte w 26 tabelach. Samo zamodelowanie produktów, wariantów, atrybutów i ich hierarchii wymagało utworzenia 8 relacji. Takie podejście powodowało konieczność licznych operacji JOIN, aby informacje pozyskiwane w zapytaniach były kompletne i użyteczne.  

W przypadku bazy dokumentowej, dzięki denormalizacji wspomniane wyżej informacje o produktach są zebrane w jednym dokumencie.

### 1.2. Reprezentacja związków między danymi
Związki między encjami w bazie relacyjnej modelowane były przy użyciu kluczy obcych i ewentualnych tabel pośredniczących.  
W bazie dokumentowej, związki modelowane są przy pomocy zagnieżdżania danych.

### 1.3. Zachowanie spójności
Baza relacyjna samodzielnie dba o spójność danych i więzy integralności, w przypadku projektu bazy dokumentowej, odpowiedzialność za to przechodzi na warstwę aplikacji.

### 1.4. Złożoność zapytań i modelu danych
W bazie relacyjnej normalizacja powodowała przeniesienie złożoności z modelu danych na zapytania - podstawowe operacje wymagały łączenia wielu tabel.  
W bazie dokumentowej złożoność leży w modelu danych - denormalizacja i zagnieżdżenie danych powoduje uproszczenie operacji odczytu kosztem bardziej złożonych operacji zapisu i aktualizacji.

## 2. Czy zastosowania projektów są tożsame i można je traktować wymiennie?
W kontekście platformy e-commerce, oba projekty w technologiach relacyjnej i nierelacyjnej realizują to samo zadanie. W ogólnym przypadku możliwe byłoby zastąpienie jednego drugim, ale znacznie lepiej jest mieć na uwadze ograniczenia i zalety obu rozwiązań.

## 3. Czy zastosowania baz relacyjnych i nierelacyjnych są tożsame i można traktować je wymiennie?
Niezależnie od wyboru technologii baza danych spełni swoje zadanie, ale może się to odbyć pod pewnym kosztem.  
Baza relacyjna sprawdzi się lepiej jako źródło prawdy, dbając o silną spójność danych (dzięki ACID), co odzwierciedlało nasze początkowe podejście do produktów jako pojedynczych instancji w bazie danych.  
Baza nierelacyjna jest idealna do danych o zmiennej strukturze (w naszym przypadku różnorodność cech produktów) oraz sytuacji wymagających szybkiego odczytu. W bazie dokumentowej spójność danych może zostać tymczasowo naruszona w celu zapewnienia ciągłej dostępności.

## 4. W jakich zastosowaniach lepiej sprawdzają się bazy relacyjne, a w jakich wybrana technologia nierelacyjna?

### 4.1. Bazy relacyjne
Bazy relacyjne sprawdzą się lepiej w:
- systemach transakcyjnych związanych z Online Transaction Processing (OLTP)
- systemach ERP - Enterprise Resource Planning
- systemach CRM - Customer Relationship Management
- zastosowaniach wymagających silnej spójności między danymi

### 4.2. Bazy dokumentowe
Bazy dokumentowe sprawdzą się w:
- systemach o zmiennej i różnorodnej strukturze danych
- prostych aplikacjach webowych
- systemach wymagających dużej skalowalności horyzontalnej

## 5. Czy pojawiła się konieczność zmiany założeń lub wybrane wymagania były niemożliwe do zrealizowania?
Wszystkie ustalone wymagania udało się zrealizować, konieczna jednak była weryfikacja niektórych założeń.

### 5.1. Dane w ramach zamówienia
Dane zamówienia (Order) zostały zmienione na historyczne - adresy i ceny produktów są kopiowane do dokumentu w momencie zakupu.  
Dzięki temu nie dochodzi do zmiany danych w starych zamówieniach.

### 5.2. Brak kluczy obcych i więzów integralności
Brak kluczy obcych i więzów integralności powoduje, że odpowiedzialność za poprawność referencji spoczywa teraz na warstwie aplikacji.

## 6. W jaki sposób wybrana baza NoSQL różni się od bazy relacyjnej pod względem definiowania zapytań?

### 6.1. PostgreSQL
W ramach PostgreSQL zapytania definiowane są przy użyciu języka SQL. W celu połączenia danych z licznych relacji konieczne było zastosowanie wielu operacji JOIN. Optymalizacja zapytań wymagała przypisania indeksów.

### 6.2. MongoDB
W MongoDB zapytania opierają się o pipeline agregacyjny: polecenia takie jak ```$match```, ```$group```, ```$unwind```, ```$lookup``` dają rezultaty podobne do instrukcji SQL ale działają bardziej proceduralnie, modyfikując wynik w ramach pipeline'u.

## 7. Jakie są główne różnice w wydajności i jakie są ich przyczyny?

### 7.1. PostgreSQL
- bardzo dobra wydajność przy złożonych zapytaniach analitycznych
- stabilne czasy odpowiedzi przy operacjach transakcyjnych
- spadek wydajności przy dużej liczbie JOIN i silnej normalizacji
- duży wpływ indeksów na plan zapytań (czasem negatywny)

### 7.2. MongoDB
- bardzo szybkie odczyty dokumentów (nie wymaga JOINów)
- dobra skalowalność horyzontalna
- większa liczba operacji zapisu przy aktualizacji zagnieżdżonych struktur
- brak kosztów planowania zapytań porównywalnych do SQL

### 7.3. Przyczyny różnic
Bazy różnią się wydajnością przez inherentnie inne modele danych - tabele a dokumenty oraz inne podejście do relacji - zagnieżdżenie powiązanych danych w przeciwieństwie do związków łączonych JOINem.