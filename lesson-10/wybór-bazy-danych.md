## Wybraną przez nas technologią jest MongoDB (baza dokumentowa).

| Typ Bazy Danych | Przykłady | Zalety (Kiedy Używać) | Wady (Ograniczenia) | Zastosowanie w Twoim E-commerce |
| :--- | :--- | :--- | :--- | :--- |
| **1. Dokumentowa** | MongoDB, Couchbase, Firestore | * **Naturalny model dla JSON:** Idealna dla złożonych, hierarchicznych danych (Karta Produktu). * **Elastyczny Schemat:** Łatwa zmiana atrybutów bez migracji. * **Wysoka Wydajność Odczytu:** Wszystkie powiązane dane w jednym dokumencie. | * **Redundancja Danych:** Wymaga ręcznej aktualizacji wielu dokumentów przy zmianie metadanych (np. nazwy producenta). * **Złożone Transakcje:** Wymaga użycia transakcji wielodokumentowych (wolniejsze niż pojedynczy zapis). | **GŁÓWNY WYBÓR:** Idealna dla **`products`**, **`users`**, **`orders`** i **`reviews`**. |
| **2. Klucz-Wartość** | Redis, Memcached, DynamoDB | * **Ekstremalna Szybkość:** Najszybsza do prostych operacji GET/PUT (odczyt/zapis). * **Wysoka Skalowalność:** Prosty model danych ułatwia horyzontalne skalowanie. * **Idealna dla Caching (pamięć podręczna):** Niskie opóźnienia. | * **Brak Relacji/Zapytań:** Nie da się wyszukiwać po wartości, tylko po kluczu. * **Brak Elastyczności:** Dane muszą być spłaszczone i z góry określone. | **WSPARCIE:** Idealna dla **`carts`** (sesje koszyków) oraz **sesji użytkowników** (jako pamięć podręczna). |
| **3. Kolumnowa (Wide-Column)** | Cassandra, HBase | * **Ekstremalna Skalowalność:** Zaprojektowana do obsługi ogromnych ilości danych na tysiącach serwerów. * **Idealna dla Time-Series:** Zapis dużej ilości danych szeregów czasowych/logów. * **Wysoka Dostępność.** | * **Złożona Konfiguracja:** Wymaga doświadczonej administracji. * **Słaba na Relacje:** Brak joinów. * **Optymalizowana pod DYSK, nie pod pamięć RAM** (wolniejsza niż Redis). | **NIEZALECANA/OPCJONALNA:** Mogłaby służyć do przechowywania **logów ruchu** lub **historii zmian magazynowych** (Event Sourcing). |
| **4. Grafowa** | Neo4j, ArangoDB | * **Wysoka Wydajność Relacji:** Zaprojektowana do analizy powiązań (np. Znajomi, Droga dostawy). * **Naturalne Modelowanie Sieci:** Idealna do rekomendacji ("Klienci, którzy kupili X, kupili również Y"). | * **Słaba na Proste Operacje:** Powolna dla prostych odczytów katalogowych. * **Skalowalność Horyzontalna:** Trudniejsza niż w bazach dokumentowych. | **NISZOWA:** Idealna do silnika **rekomendacji** produktów, ale nie do głównego katalogu. |

---

Postawiliśmy na bazę danych dukumentową, ponieważ nasz sklep jest często odczytywany, a rzedziej modyfikowany. Dodatkowo struktura "Warianty-Opcje-Atrybuty" w SQL jest skomplikowana i wolna, w przeciwieństwie do MongoDB gdzie jest to narutalna struktura JSON.

## Wybór i uzasadnienie technologii
Wybrana technologia: **Baza dokumentowa MongoDB**.

### Zalety wybranej bazy:

**Wydajność "Karty Produktu":** W modelu relacyjnym pobranie produktu wraz z wariantami, atrybutami, producentem i kategoriami wymaga złączenia (JOIN) wielu tabel. W MongoDB wszystkie te dane są w jednym dokumencie (products), co pozwala na pobranie ich jednym, błyskawicznym zapytaniem.

**Elastyczność Schematu:** Sklep oferuje różne typy produktów (np. elektronika vs odzież). W MongoDB każdy produkt może mieć inny zestaw atrybutów w polu attributes (np. rozmiar dla butów, taktowanie CPU dla laptopa) bez konieczności tworzenia skomplikowanej struktury, która była konieczna w SQL.

**Skalowalność Horyzontalna:** Kolekcje takie jak users czy reviews mogą rosnąć do milionów rekordów. MongoDB obsługuje sharding (podział danych na wiele serwerów), co zabezpiecza projekt na przyszły wzrost ruchu.

### Wady wybranej bazy:

**Trudniejsza obsługa stanów magazynowych:** Tabele SQL SerialStockItem i OrderStockAllocation zapewniały ścisłą kontrolę nad każdym egzemplarzem towaru. W MongoDB zarządzanie unikalnością numerów seryjnych w tablicach wewnątrz dokumentu wymaga skomplikowanych operacji aktualizacji, aby uniknąć błędów współbieżności (race conditions).

**Redundancja danych:** Nazwa producenta ("Nike") czy kategorii jest powielona w tysiącach produktów. Zmiana nazwy producenta wymaga aktualizacji tysięcy dokumentów, a nie jednego wiersza jak w SQL.

## Weryfikacja przyjętych założeń i ograniczeń
### Założenie 1: Denormalizacja Zamówień

**Treść:** Założono, że dane w zamówieniu (Order) nie powinny być relacyjne, lecz historyczne. Dlatego adresy i ceny produktów są kopiowane do dokumentu zamówienia w momencie zakupu.

**Weryfikacja:** Podejście to eliminuje błędy biznesowe (np. zmiana ceny produktu w bazie nie zmienia ceny w starych zamówieniach).

### Założenie 2: Modelowanie Magazynu

**Treść:** Założono uproszczenie modelu magazynowego poprzez przechowywanie stanów ilościowych wewnątrz dokumentów magazynów (inventory), zamiast śledzenia każdej sztuki jako osobnego rekordu relacyjnego.

**Ograniczenie:** To podejście utrudnia śledzenie historii ruchu konkretnego numeru seryjnego.

**Wniosek:** Dla potrzeb e-commerce priorytetem jest szybkość sprawdzenia dostępności ("Czy towar jest?"), co ten model spełnia. Pełna historia ruchu magazynowego musiałaby być realizowana przez dodatkowy system logów (Event Sourcing), co wykracza poza ramy podstawowej bazy NoSQL.

### Założenie 3: Brak Transakcji między wieloma kolekcjami

**Treść:** W starszych wersjach NoSQL brakowało transakcji ACID.

**Weryfikacja:** Nowoczesne MongoDB obsługuje transakcje wielodokumentowe. Projekt zakłada ich użycie w krytycznym momencie składania zamówienia (zmniejszenie stanu w inventory i utworzenie order), co niweluje główną wadę NoSQL w zastosowaniach finansowych.
