# Projekt Bazy Danych

Repozytorium zawiera projekt **baz danych** realizowany zarówno w technologii **relacyjnej**, jak i **nierelacyjnej (NoSQL)**. Projekt jest realizowany zespołowo przez cztery osoby: **Anna Kępowicz, Błażej Kowal, Dawid Błaszczyk, Kacper Mocek**.  

## Zawartość repozytorium

### 1. Faza konceptualna
- Streszczenie wymagań projektu i zakres działań.
- Specyfikacja funkcjonalna z mechanizmem logowania użytkowników i różnymi poziomami dostępu (min. 4 role: admin, user, editor, itp.).
- Diagram obiektowo-związkowy (ER) z ok. 20 encjami, relacjami 1-N i N-N.

### 2. Faza logiczna
- Definicja schematów relacji na podstawie diagramu ER.
- Normalizacja do III postaci normalnej.
- Diagram relacji przygotowany w narzędziu do projektowania baz danych.

### 3. Faza fizyczna
- Skrypty SQL DDL do tworzenia bazy relacyjnej, z więzami integralności i ograniczeniami (CHECK, kaskady).
- Skrypt w Pythonie (lub innym języku) generujący losowe dane dla bazy relacyjnej, obsługujący powiązania między encjami.
- Raporty i funkcje wyszukiwania – minimum 20 zapytań SQL o różnym charakterze, w tym statystycznym.
- Analiza zapytań przy użyciu funkcji `EXPLAIN` i wprowadzenie indeksów.
- Sprawozdanie powykonawcze z wnioskami dotyczącymi realizacji projektu i kierunków rozwoju bazy.
- Aktualizacje bazy i raportów w przypadku zmiany wymagań.

### 4. Projekt bazy nierelacyjnej (NoSQL)
- Wybór technologii NoSQL oraz uzasadnienie decyzji (zalety i wady).
- Implementacja struktur przechowywania danych, mechanizmów spójności i zapytań.
- Skrypt generujący losowe dane dla bazy NoSQL.
- Raporty i funkcje wyszukiwania – minimum 20 zapytań, w tym statystycznych.
- Analiza porównawcza z bazą relacyjną – różnice w wydajności, sposobie definiowania zapytań i realizacji wymagań.

