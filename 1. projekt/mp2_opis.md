# MP2: Czyszczenie danych i feature engineering

## Scenariusz

Zapoznałeś się z danymi MajsterPlus i zidentyfikowałeś kilka problemów jakości: polskie formaty dat, ciągi walutowe, brakujące wartości, wartości odstające i niemożliwe wartości. Teraz musisz **oczyścić i przetransformować** dane do formatu odpowiedniego dla machine learning.

Ten mini-projekt obejmuje fazę **Data Preparation** z CRISP-DM — najbardziej pracochłonną fazę w każdym projekcie data science.

## Cele dydaktyczne

Po ukończeniu tego mini-projektu powinieneś umieć:
- Parsować niestandardowe formaty dat i ciągi walutowe
- Identyfikować i obsługiwać różne typy brakujących danych
- Wykrywać i usuwać wartości odstające za pomocą metody IQR
- Kodować zmienne kategoryczne (binarne, porządkowe, one-hot encoding)
- Zastosować skalowanie cech (StandardScaler) z prawidłowym podziałem train/test

## Co otrzymujesz

- `3. notatniki/mp2_starter.ipynb` — notatnik startowy z 12-krokowym pipeline
- `2. data/customers.csv` — surowe dane (lub użyj `2. data/checkpoints/checkpoint_for_mp2.csv`)
- `2. data/data_dictionary.md` — dokumentuje wszystkie 10 problemów jakości danych

## Co robisz

Musisz postępować zgodnie z **obowiązkową 12-krokową kolejnością przetwarzania**. Zmiana kolejności spowoduje inne wyniki.

| Krok | Zadanie | Uzupełnione? | Szacowany czas |
|------|---------|-------------|---------------|
| 1-2 | Załaduj dane i zweryfikuj sumę MD5 | Tak | 5 min |
| 3 | Oddziel zmienną docelową, usuń customer_id | Tak | 5 min |
| 4 | Parsuj polskie daty (helper udostępniony) | **TODO: zastosuj** | 15 min |
| 5 | Oczyść total_spend (ciąg PLN → float) | **TODO** | 10 min |
| 6 | Zamień niemożliwe satisfaction_score na NaN | **TODO** | 10 min |
| 7 | Imputuj brakujące wartości (mediana/moda) | **TODO** | 20 min |
| 8 | Usuń wartości odstające IQR z avg_basket_value | **Częściowo uzupełnione, TODO: filtruj** | 15 min |
| 9 | Zakoduj zmienne kategoryczne (binarne, porządkowe, one-hot) | **TODO** | 25 min |
| 10 | Bramka asercji null | Tak | 2 min |
| 11 | Train/test split (80/20, stratified) | Tak | 5 min |
| 12 | StandardScaler (dopasuj tylko na train) | **TODO** | 10 min |
| Bonus | Clustering K-Means (opcjonalnie) | **TODO** | 15 min |
| Zapis | Checkpoint dla MP3 | Tak | 2 min |
| | **Razem** | | **~2,5 godziny** |

## Co oddajesz

**10 odpowiedzi MCQ** przez LMS (okno 48 godzin, 3 próby).

### Zanim rozpoczniesz test, powinieneś rozumieć:

- [ ] Co średnia vs mediana `total_spend` mówi o kształcie rozkładu
- [ ] Dlaczego niemożliwe wartości `satisfaction_score` muszą zostać zamienione na NaN *przed* imputation medianą (kolejność pipeline)
- [ ] Dlaczego filtrowanie `y` i `gender_series` po usunięciu wartości odstających IQR jest kluczowe (wyrównanie)
- [ ] Kompromis między `drop_first=False` a `drop_first=True` w one-hot encoding
- [ ] Wymiary zbioru treningowego (wiersze × cechy)

## Wskazówki i typowe błędy

1. **Postępuj dokładnie w podanej kolejności.** Krok 6 (niemożliwe wartości → NaN) musi nastąpić PRZED krokiem 7 (imputation). W przeciwnym razie niemożliwe wartości zostaną zaimputowane, a nie zastąpione.

2. **Helper do polskich dat jest udostępniony** — musisz go tylko zastosować za pomocą `.apply(parse_polish_date)`.

3. **Konwersja total_spend**: Najpierw usuń „PLN " (zwróć uwagę na spację po PLN), następnie usuń przecinki, potem rzutuj na float.

4. **Satisfaction score**: Poprawny zakres to [1.0, 5.0]. Wartości poza tym zakresem (0.0, 7.2, -1.0) to błędy wprowadzania danych. Zamień na NaN, a następnie imputuj razem z innymi brakującymi wartościami.

5. **Usuwanie wartości odstających IQR**: Obliczenie IQR jest uzupełnione. Musisz zastosować filtr. **Nie zapomnij** również przefiltrować `y` (cel) i `gender_series`, aby utrzymać je wyrównane.

6. **Kolejność kodowania ma znaczenie**:
   - Najpierw: `loyalty_member` → binarne (Tak=1, Nie=0)
   - Następnie: `monthly_income_bracket` → porządkowe (A=1, B=2, ..., E=5)
   - Na końcu: pozostałe kategoryczne → `pd.get_dummies(drop_first=False)`
   - **Posortuj kolumny alfabetycznie** po kodowaniu: `df = df[sorted(df.columns)]`

7. **`drop_first=False`** — zachowujemy wszystkie kolumny dummy dla przejrzystości dydaktycznej. To jest celowe.

8. **Kolumny boolean**: Po `pd.get_dummies()` niektóre kolumny mogą być typu boolean. Skonwertuj je na int: `df[bool_cols] = df[bool_cols].astype(int)`

9. **StandardScaler**: Dopasuj TYLKO na danych treningowych, transformuj zarówno train, jak i test. Dopasowanie na pełnych danych = data leakage.

10. **Zweryfikuj swoje wyniki**: Uruchom `3. notatniki/skrypty/verify_checkpoint.py`, aby porównać z bazowym punktem kontrolnym. Powie Ci dokładnie, co się różni.

## Jeśli Twoje wyniki się różnią

Jeśli Twoje wyniki nie zgadzają się z oczekiwanymi wartościami i nie możesz znaleźć przyczyny:
1. Uruchom `3. notatniki/skrypty/verify_checkpoint.py` po szczegółowe komunikaty o błędach
2. Jeśli nadal utkniesz, załaduj bazowy checkpoint `2. data/checkpoints/checkpoint_for_mp3.pkl` i przejdź do MP3

## Reprodukowalność

- Random seed: 42
- Kolejność przetwarzania: Kroki 1-12 jak określono
- `pd.get_dummies(drop_first=False)` — zachowaj wszystkie dummy
- Kolumny posortowane alfabetycznie po kodowaniu
- StandardScaler dopasowany tylko na train
