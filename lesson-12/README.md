# MongoDB Data Generator

Generator danych dla bazy danych MongoDB zgodny z walidacjami zdefiniowanymi w `lesson-11/validations.md`.

## Instalacja

1. Zainstaluj zależności:
```bash
pip install -r requirements.txt
```

## Konfiguracja

1. **Liczba dokumentów**: Edytuj plik `counts.json`, aby ustawić ile dokumentów każdego typu ma być wygenerowane.

2. **Połączenie z MongoDB**: 
   - Domyślnie: `mongodb://localhost:27017/`
   - Możesz ustawić zmienne środowiskowe:
     - `MONGO_URI` - URI połączenia z MongoDB
     - `DATABASE_NAME` - nazwa bazy danych (domyślnie: `ecommerce_db`)

## Uruchomienie

```bash
python main.py
```

Skrypt wygeneruje dane w następującej kolejności (zachowując spójność referencyjną):

1. Manufacturers (producenci)
2. Warehouses (magazyny)
3. Users (użytkownicy)
4. Products (produkty z wariantami)
5. Promotions (promocje)
6. Inventory Bulk (magazyn zbiorczy)
7. Inventory Serial (magazyn seryjny)
8. Carts (koszyki)
9. Orders (zamówienia)
10. Reviews (recenzje)
11. User Favorites (ulubione produkty)

## Struktura danych

Wszystkie generowane dane są zgodne z walidacjami zdefiniowanymi w `lesson-11/validations.md`:

- **Carts**: Koszyki użytkowników z produktami
- **Inventory Bulk**: Magazyn zbiorczy dla produktów
- **Inventory Serial**: Magazyn seryjny z numerami seryjnymi
- **Manufacturers**: Producenci produktów
- **Orders**: Zamówienia użytkowników
- **Products**: Produkty z wariantami, kategoriami i atrybutami
- **Promotions**: Promocje i zniżki
- **Reviews**: Recenzje produktów
- **User Favorites**: Ulubione produkty użytkowników
- **Users**: Użytkownicy z adresami i rolami
- **Warehouses**: Magazyny z lokalizacjami

## Spójność danych

Generator zapewnia spójność danych:
- Produkty mają warianty i są powiązane z producentami
- Warianty produktów są dostępne w magazynach (bulk lub serial)
- Zamówienia odnoszą się do istniejących użytkowników i produktów
- Koszyki zawierają produkty dostępne w systemie
- Recenzje są przypisane do istniejących produktów i użytkowników
