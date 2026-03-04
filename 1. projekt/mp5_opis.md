# MP5: Porównanie modeli i końcowa rekomendacja

## Scenariusz

Zbudowałeś i zewaluowałeś dwa modele. Teraz MajsterPlus prosi o Twoją **końcową rekomendację**: Który model powinniśmy wdrożyć? Przy jakim threshold? A co z fairness między grupami demograficznymi? Wiceprezes ds. marketingu potrzebuje pisemnej rekomendacji, którą może przedstawić zarządowi.

Ten mini-projekt obejmuje fazę **Evaluation** z CRISP-DM — syntezę, porównanie i rekomendację.

## Cele dydaktyczne

Po ukończeniu tego mini-projektu powinieneś umieć:
- Wytrenować i zewaluować dodatkowe algorytmy (GradientBoosting, VotingClassifier)
- Porównać modele pod kątem wielu kryteriów (statystyki, zysk, fairness, interpretowalność)
- Ocenić fairness modelu analizując wydajność w podgrupach demograficznych
- Ocenić interpretowalność modelu (współczynniki vs. feature importance)
- Napisać ustrukturyzowaną, opartą na dowodach rekomendację biznesową

## Co otrzymujesz

- `3. notatniki/mp5_starter.ipynb` — minimalny szkielet, głównie nagłówki sekcji
- Checkpoint z MP4 (`checkpoints/mp4_checkpoint.pkl` lub `2. data/checkpoints/checkpoint_for_mp5.pkl`)

**Jeśli nie ukończyłeś MP4**, załaduj bazowy checkpoint:
```python
import pickle
with open("../2. data/checkpoints/checkpoint_for_mp5.pkl", "rb") as f:
    checkpoint = pickle.load(f)
```

## Co robisz

| Krok | Zadanie | Uzupełnione? | Szacowany czas |
|------|---------|-------------|---------------|
| 1 | Załaduj checkpoint | Tak | 5 min |
| 2-3 | Wykorzystaj modele LR + RF z checkpointu | Tak | 5 min |
| 4 | **TODO**: Wytrenuj GradientBoostingClassifier | **TODO** | 15 min |
| 5 | **TODO**: Utwórz VotingClassifier (opcjonalnie) | **TODO** | 15 min |
| 6 | **TODO**: Tabela porównania wielokryterialnego | **TODO** | 20 min |
| 7 | **TODO**: Porównanie zysku biznesowego (wszystkie modele, optymalne thresholds) | **TODO** | 20 min |
| 8 | **TODO**: Analiza fairness (recall/precision wg płci) | **TODO** | 20 min |
| 9 | **TODO**: Ocena interpretowalności | **TODO** | 15 min |
| 10 | **TODO**: Napisz końcową rekomendację | **TODO** | 20 min |
| | **Razem** | | **~2,5 godziny** |

## Co oddajesz

**10 odpowiedzi MCQ** przez LMS (okno 48 godzin, 3 próby).

### Zanim rozpoczniesz test, powinieneś rozumieć:

- [ ] Dlaczego model z najwyższym ROC-AUC niekoniecznie generuje najwyższy zysk biznesowy
- [ ] Jakie dodatkowe kryteria (poza AUC) powinny kierować wyborem modelu, gdy AUC są prawie identyczne
- [ ] ROC-AUC VotingClassifier i który model ma najwyższe ROC-AUC ogólnie
- [ ] Różnicę recall między grupami płci dla GradientBoosting
- [ ] Który model zarekomendowałbyś do wdrożenia i dlaczego (zysk, interpretowalność, fairness)

## Wskazówki i typowe błędy

1. **GradientBoosting**: Użyj `GradientBoostingClassifier(random_state=42)` z domyślnymi hiperparametrami. Inny random_state = inne wyniki.

2. **VotingClassifier**: Użyj `voting="soft"`, aby uśredniać prawdopodobieństwa (nie twarde głosy). Uwzględnij LR, RF i GB jako estymatory.

3. **Najlepszy ROC-AUC ≠ najlepszy model biznesowy.** To kluczowa obserwacja tego MP. Model z najwyższym AUC może nie generować największego zysku, gdy zastosowana jest cost matrix. Porównuj przy optymalnym threshold każdego modelu.

4. **Analiza fairness**: Seria `gender_test` jest w checkpoincie. Użyj jej do podziału predykcji wg płci (M/K) i oblicz recall oraz precision dla każdej podgrupy. Różnica > 0.05 między grupami zasługuje na omówienie.

5. **Ranking interpretowalności**:
   - Logistic Regression: najbardziej interpretowalny (bezpośrednie współczynniki ze znakiem i wielkością)
   - GradientBoosting/RandomForest: feature importance pokazują *co* ma znaczenie, ale nie *jak*
   - VotingClassifier: najmniej interpretowalny (łączy wiele modeli)

6. **Struktura końcowej rekomendacji**:
   - Który model i dlaczego
   - Jaki threshold
   - Oczekiwany wpływ finansowy
   - Zastrzeżenia i ograniczenia
   - Sugerowane kolejne kroki

7. **Wzorzec „prostszy model wygrywa"**: Nie zdziw się, jeśli LogisticRegression generuje najwyższy zysk. Przy ciasnych marżach (60 PLN na TP vs. 80 PLN na FP) konserwatywny, precyzyjny model może przewyższyć złożony.

8. **Opcjonalna sekcja PyCaret** jest nieoceniana. Eksploruj ją tylko, jeśli masz czas i chęci.

## Jeśli Twoje wyniki się różnią

Jeśli Twoje metryki nie zgadzają się:
1. Sprawdź `GradientBoostingClassifier(random_state=42)` — domyślne hiperparametry
2. Zweryfikuj, że VotingClassifier używa `voting="soft"` z dokładnie [lr, rf, gb] jako estymatorami
3. Upewnij się, że używasz tego samego CAMPAIGN_COST (80) i EXPECTED_REVENUE z checkpointu

## Reprodukowalność

- Random seed: 42 (dla GradientBoosting)
- VotingClassifier: soft voting, estymatory = [LR, RF, GB]
- Ta sama cost matrix co w MP4 (koszt kampanii = 80 PLN, przychód z checkpointu)
