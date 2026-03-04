# MP3: Modelowanie baseline i porównanie algorytmów

## Scenariusz

Twoje dane są czyste i gotowe do modelowania. MajsterPlus musi wiedzieć: **czy możemy przewidzieć, którzy klienci odejdą?** Wytrenujesz dwa różne algorytmy — Logistic Regression (prosty, interpretowalny) i Random Forest (złożony, wydajny) — i porównasz ich wydajność.

Ten mini-projekt obejmuje fazę **Modeling** z CRISP-DM.

## Cele dydaktyczne

Po ukończeniu tego mini-projektu powinieneś umieć:
- Trenować modele klasyfikacji z użyciem scikit-learn
- Ewaluować modele za pomocą confusion matrix, classification report i ROC-AUC
- Porównywać modele za pomocą krzywych ROC na jednym wykresie
- Analizować feature importance z modeli drzewiastych
- Wykrywać overfitting porównując wydajność na train vs. test

## Co otrzymujesz

- `3. notatniki/mp3_starter.ipynb` — notatnik startowy z nagłówkami sekcji i wskazówkami
- Checkpoint z MP2 (`checkpoints/mp2_checkpoint.pkl` lub `2. data/checkpoints/checkpoint_for_mp3.pkl`)

**Jeśli nie ukończyłeś MP2**, załaduj bazowy checkpoint:
```python
import pickle
with open("../2. data/checkpoints/checkpoint_for_mp3.pkl", "rb") as f:
    checkpoint = pickle.load(f)
```

## Co robisz

| Krok | Zadanie | Uzupełnione? | Szacowany czas |
|------|---------|-------------|---------------|
| 1 | Załaduj checkpoint | Tak | 5 min |
| 2 | **TODO**: Wytrenuj LogisticRegression, oceń (confusion matrix, raport, ROC-AUC) | **TODO** | 30 min |
| 3 | **TODO**: Wytrenuj RandomForest, oceń tymi samymi metrykami | **TODO** | 25 min |
| 4 | **TODO**: Wykreśl krzywe ROC dla obu modeli na jednym wykresie | **TODO** | 15 min |
| 5 | **TODO**: Wyodrębnij i zwizualizuj feature importance RF (top 15) | **TODO** | 15 min |
| 6 | **TODO**: Porównaj accuracy na train vs. test (sprawdzenie overfitting) | **TODO** | 10 min |
| 7 | **TODO**: Utwórz tabelę podsumowującą porównanie | **TODO** | 15 min |
| 8 | Zapisz checkpoint dla MP4 | Tak | 5 min |
| | **Razem** | | **~2 godziny** |

## Co oddajesz

**10 odpowiedzi MCQ** przez LMS (okno 48 godzin, 3 próby).

### Zanim rozpoczniesz test, powinieneś rozumieć:

- [ ] Jak interpretować confusion matrix w kontekście biznesowym MajsterPlus (znaczenie TP/FP/FN/TN)
- [ ] Co oznacza skromna poprawa AUC z baseline MP1 (~0.83) do LR w MP3 (~0.84) w kontekście sygnału predykcyjnego
- [ ] Accuracy LogisticRegression na zbiorze testowym
- [ ] Recall RandomForest dla klasy 1 (nieaktywni)
- [ ] Najważniejsza cecha wg RandomForest
- [ ] Accuracy na zbiorze treningowym dla obu modeli (sprawdzenie overfitting)

## Wskazówki i typowe błędy

1. **Użyj dokładnych hiperparametrów**:
   - `LogisticRegression(random_state=42, max_iter=1000)`
   - `RandomForestClassifier(random_state=42, n_estimators=100)`
   - Inne hiperparametry → inne wyniki → złe odpowiedzi MCQ.

2. **Interpretacja confusion matrix**: Wiersze to klasy rzeczywiste, kolumny to klasy przewidywane (domyślnie w sklearn). Więc `confusion_matrix(y_test, y_pred)` daje:
   ```
   [[TN, FP],
    [FN, TP]]
   ```

3. **Krzywe ROC**: Użyj `RocCurveDisplay.from_predictions()` do tworzenia przejrzystych wykresów. Wykreśl obie na tym samym `ax` do porównania.

4. **Feature importance**: `rf.feature_importances_` daje ważność dla każdej cechy w kolejności, w jakiej pojawiają się w danych treningowych. Zmapuj je na nazwy cech.

5. **Sprawdzenie overfitting**: Random Forest osiągający 100% accuracy na train jest częsty i oczekiwany — zapamiętuje dane treningowe domyślnie. Kluczowe pytanie to, o ile gorszy jest na zbiorze testowym.

6. **Precision vs. Recall**: Nie myl ich:
   - **Precision** = TP / (TP + FP) — „Spośród przewidywanych jako nieaktywni, ilu naprawdę jest?"
   - **Recall** = TP / (TP + FN) — „Spośród naprawdę nieaktywnych, ilu wyłapaliśmy?"

7. **Zapisz swoje modele** w checkpoincie — będą Ci potrzebne w MP4 i MP5.

## Jeśli Twoje wyniki się różnią

Jeśli Twoje metryki nie zgadzają się z oczekiwanymi wartościami:
1. Sprawdź, czy załadowałeś poprawny checkpoint (wynik MP2 lub bazowy)
2. Sprawdź, czy hiperparametry zgadzają się dokładnie (random_state=42, max_iter=1000, n_estimators=100)
3. Jeśli nadal utkniesz, załaduj `2. data/checkpoints/checkpoint_for_mp4.pkl`, aby kontynuować z MP4

## Reprodukowalność

- Random seed: 42 (dla wszystkich modeli)
- LogisticRegression: `max_iter=1000`
- RandomForest: `n_estimators=100`
