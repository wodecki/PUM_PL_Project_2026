# MP1: Kontekst biznesowy i eksploracja danych

## Scenariusz

MajsterPlus udostępnił Ci dwa zbiory danych zawierające dane demograficzne klientów, zachowania zakupowe i rekordy transakcji. Zanim zaczniesz budować jakiekolwiek modele, musisz **zrozumieć dane**: ich strukturę, rozkłady, problemy jakości i to, czy jest wystarczający sygnał do przewidywania odejścia klienta.

Ten mini-projekt obejmuje fazy **Business Understanding** i **Data Understanding** z CRISP-DM.

## Cele dydaktyczne

Po ukończeniu tego mini-projektu powinieneś umieć:
- Załadować i zweryfikować integralność zbiorów danych za pomocą sum MD5
- Zidentyfikować typy kolumn, wzorce brakujących wartości i problemy jakości danych
- Zwizualizować rozkłady i korelacje, aby zrozumieć zależności między cechami
- Wytrenować prosty model baseline, aby ocenić możliwość uczenia

## Co otrzymujesz

- `3. notatniki/mp1_starter.ipynb` — notatnik startowy z uzupełnionymi komórkami i placeholderami `# TWÓJ KOD TUTAJ`
- `2. data/customers.csv` — 5 000 rekordów klientów (21 kolumn)
- `2. data/transactions.csv` — ~25 000 rekordów transakcji (8 kolumn)
- `2. data/data_dictionary.md` — pełna dokumentacja kolumn

## Co robisz

| Krok | Zadanie | Szacowany czas |
|------|---------|---------------|
| 1 | Uruchom komórki konfiguracyjne (blokady reprodukowalności, importy, ładowanie danych) | 5 min |
| 2 | Zbadaj kształt, typy danych i pierwsze wiersze — uzupełnione | 10 min |
| 3 | **TODO**: Przeanalizuj brakujące wartości we wszystkich kolumnach | 15 min |
| 4 | Przejrzyj rozkład zmiennej docelowej (uzupełnione) | 5 min |
| 5 | **TODO**: Utwórz mapę cieplną korelacji cech numerycznych | 20 min |
| 6 | **TODO**: Utwórz wykresy zależności (boxploty, histogramy) | 25 min |
| 7 | Przejrzyj model baseline „sneak peek" (uzupełnione) | 10 min |
| 8 | **TODO**: Napisz 3-5 kluczowych obserwacji | 20 min |
| | **Razem** | **~2 godziny** |

## Co oddajesz

**10 odpowiedzi MCQ** przez Edux (okno 48 godzin, 3 próby).

### Zanim rozpoczniesz test, powinieneś rozumieć:

- [ ] Relację między `customers.csv` (5 000 wierszy) a `transactions.csv` (~25 000 wierszy) — co oznacza ten stosunek
- [ ] Dlaczego wysoka accuracy może być myląca na niezbalansowanych danych (~19,5% odejść)
- [ ] Które kolumny mają brakujące wartości, która ma ich najwięcej i dlaczego wzorce brakujących wartości mają znaczenie
- [ ] Co oznaczają skrajne wartości odstające w `avg_basket_value` i jak wpływają na modelowanie
- [ ] Wynik ROC-AUC modelu baseline (~0.83) i co mówi o możliwości uczenia

## Wskazówki i typowe błędy

1. **Przeczytaj najpierw `2. data/data_dictionary.md`.** Dokumentuje wszystkie 21 kolumn, ich typy, zakresy i celowe problemy jakości danych.

2. **Nie próbuj naprawiać problemów jakości danych w MP1.** Ten mini-projekt dotyczy ich *odkrycia*. Naprawa nastąpi w MP2.

3. **Kolumna `total_spend` jest ciągiem tekstowym**, nie liczbą. Zawiera wartości typu „PLN 1,234.50". Zajmiesz się tym w MP2.

4. **`registration_date` używa polskich skrótów miesięcy** (sty, lut, mar, ...). Standardowy `pd.to_datetime()` ich nie sparsuje.

5. **Model baseline wyklucza `days_since_last_purchase`** celowo — jest quasi-deterministyczny ze zmienną docelową (odejście definiowane jako > 90 dni od ostatniego zakupu). Jego uwzględnienie zawyżyłoby metryki.

6. **Mapa cieplna korelacji**: Szukaj zarówno silnych korelacji pozytywnych, JAK I negatywnych. Kilka par ma |r| > 0.5.

## Reprodukowalność

- Random seed: 42 (ustawiony w pierwszej komórce)
- NIE modyfikuj blokad reprodukowalności ani komórek ładowania danych
- Twoje wyniki powinny dokładnie odpowiadać notatnikowi rozwiązania
