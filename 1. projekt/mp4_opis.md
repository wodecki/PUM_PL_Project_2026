# MP4: Ewaluacja modelu i wpływ biznesowy

## Scenariusz

Wytreniowałeś dwa modele. Ale MajsterPlus nie interesuje ROC-AUC — interesują ich **pieniądze**. Wiceprezes ds. marketingu pyta: „Jeśli uruchomimy kampanię reaktywacyjną celującą w predykcje Twojego modelu, ile zysku osiągniemy? I czy powinniśmy kontaktować wszystkich, czy tylko klientów wysokiego ryzyka?"

Ten mini-projekt obejmuje fazę **Evaluation** z CRISP-DM — przekładanie metryk statystycznych na wartość biznesową.

## Cele dydaktyczne

Po ukończeniu tego mini-projektu powinieneś umieć:
- Zbudować cost matrix mapującą predykcje na wyniki finansowe
- Obliczyć zysk na rekord przy danym classification threshold
- Porównać celowanie oparte na modelu z naiwnymi strategiami (kontaktuj wszystkich / nikogo)
- Zoptymalizować classification threshold dla maksymalnego zysku
- Zinterpretować krzywe cumulative gains (lift)

## Co otrzymujesz

- `3. notatniki/mp4_starter.ipynb` — notatnik startowy z kontekstem biznesowym i nagłówkami sekcji
- Checkpoint z MP3 (`checkpoints/mp3_checkpoint.pkl` lub `2. data/checkpoints/checkpoint_for_mp4.pkl`)

**Jeśli nie ukończyłeś MP3**, załaduj bazowy checkpoint:
```python
import pickle
with open("../2. data/checkpoints/checkpoint_for_mp4.pkl", "rb") as f:
    checkpoint = pickle.load(f)
```

## Parametry biznesowe

| Parametr | Wartość |
|----------|---------|
| Koszt kampanii na klienta | **80 PLN** (voucher + koszty operacyjne) |
| Wartość vouchera | 50 PLN |
| Oczekiwany przychód na reaktywację | **Mediana total_spend nieaktywnych klientów w zbiorze testowym** |

**Cost matrix:**

| | Rzeczywiście nieaktywny | Rzeczywiście aktywny |
|---|---|---|
| **Skontaktowany** (przewidziany nieaktywny) | Przychód − 80 PLN (TP) | −80 PLN (FP) |
| **Nieskontaktowany** (przewidziany aktywny) | 0 PLN (FN) | 0 PLN (TN) |

## Co robisz

| Krok | Zadanie | Uzupełnione? | Szacowany czas |
|------|---------|-------------|---------------|
| 1 | Załaduj checkpoint | Tak | 5 min |
| 2 | Ustaw parametry biznesowe (koszt, przychód) | Częściowo | 10 min |
| 3 | **TODO**: Zdefiniuj funkcję compute_profit() | **TODO** | 15 min |
| 4 | **TODO**: Oblicz zysk przy threshold=0.5 dla obu modeli | **TODO** | 15 min |
| 5 | **TODO**: Oblicz zyski baseline (kontaktuj wszystkich / nikogo) | **TODO** | 10 min |
| 6 | **TODO**: Optymalizacja threshold (przeszukaj 0.05–0.95) | **TODO** | 25 min |
| 7 | **TODO**: Zidentyfikuj optymalny threshold | **TODO** | 10 min |
| 8 | **TODO**: Utwórz krzywą lift (cumulative gains) | **TODO** | 20 min |
| 9 | **TODO**: Oszacuj roczny zysk dla pełnej bazy klientów | **TODO** | 10 min |
| 10 | Zapisz checkpoint dla MP5 | Tak | 5 min |
| | **Razem** | | **~2 godziny** |

## Co oddajesz

**10 odpowiedzi MCQ** przez LMS (okno 48 godzin, 3 próby).

### Zanim rozpoczniesz test, powinieneś rozumieć:

- [ ] Oczekiwany przychód na reaktywację (mediana wydatków nieaktywnych klientów testowych)
- [ ] Zysk ze strategii „kontaktuj wszystkich" na zbiorze testowym
- [ ] Zysk LogisticRegression przy threshold 0.5
- [ ] Dlaczego threshold poniżej 0.5 może być optymalny — zależność między zyskiem z TP, kosztem FP a zyskiem
- [ ] Lift na poziomie 20% kontaktu (krzywa cumulative gains RF)

## Wskazówki i typowe błędy

1. **Oczekiwany przychód**: Użyj **mediany** total_spend nieaktywnych klientów w zbiorze testowym (nie wszystkich klientów, nie średniej). Musisz załadować surowe dane, aby uzyskać oryginalne wartości total_spend (checkpoint ma przeskalowane wartości).

2. **Strategia „kontaktuj wszystkich" przynosi straty.** To realistyczne — gdy oczekiwany przychód na klienta jest tylko nieznacznie powyżej kosztu kampanii, kontaktowanie 80% aktywnych klientów jest bardzo kosztowne.

3. **Threshold = 0.5 NIE jest optymalny.** Celem tego MP jest znalezienie lepszego threshold. Wykreśl zysk vs. threshold i znajdź szczyt.

4. **Zrozum mechanikę threshold.** Pytania MCQ sprawdzają Twoje zrozumienie, dlaczego optymalny threshold różni się od 0.5 i kompromis zysków przy threshold 0.5.

5. **Krzywa lift**: Posortuj klientów wg przewidywanego prawdopodobieństwa (najwyższe najpierw), następnie wykreśl skumulowany % wyłapanych nieaktywnych klientów vs. % skontaktowanych klientów. Im bliżej krzywa jest lewego górnego rogu, tym lepszy model.

6. **Ekstrapolacja rocznego zysku**: Zbiór testowy to ~20% pełnej bazy klientów. Skaluj proporcjonalnie: `annual = test_profit / test_fraction`.

7. **Ujemny zysk jest możliwy** i realistyczny. Jeśli false positives (80 PLN koszt każdy) przewyższają true positives, kampania traci pieniądze przy tym threshold.

## Jeśli Twoje wyniki się różnią

Jeśli Twoje obliczenia zysku nie zgadzają się:
1. Zweryfikuj, że oczekiwany przychód = mediana total_spend nieaktywnych klientów testowych (nie średnia, nie wszyscy klienci)
2. Sprawdź funkcję compute_profit: TP × (przychód − koszt) + FP × (−koszt)
3. Jeśli nadal utkniesz, załaduj `2. data/checkpoints/checkpoint_for_mp5.pkl`, aby kontynuować z MP5

## Reprodukowalność

- Koszt kampanii: 80 PLN (stały)
- Oczekiwany przychód: mediana total_spend nieaktywnych klientów testowych (deterministyczny)
- Thresholds: np.arange(0.05, 1.0, 0.05) — 19 kroków
