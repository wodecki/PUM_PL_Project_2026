# PUM: Projektowanie Usług z Wykorzystaniem Metod AI

## O czym to jest?

Jesteś **analitykiem danych** w **MajsterPlus**, polskiej sieci sklepów budowlanych z 12 placówkami. Około 18% klientów jest nieaktywnych (brak zakupu od ponad 90 dni). Twoja misja: zbudować model machine learning, który przewiduje zagrożonych klientów i zaproponować kampanię reaktywacyjną.

Zrealizujesz **5 mini-projektów (MP1-MP5)** zgodnie z metodyką CRISP-DM — od eksploracji surowych danych po końcową rekomendację biznesową.

## Struktura katalogów

```
├── 1. projekt/
│   ├── 1. scenariusz_biznesowy.md    # Historia MajsterPlus
│   ├── 2. opis_projektu.md           # Przegląd mini-projektów i model oceniania
│   ├── 3. konfiguracja_srodowiska.md # Przewodnik konfiguracji Colab / lokalnie
│   └── mp1_opis.md — mp5_opis.md     # Instrukcja krok po kroku dla każdego MP
├── 2. data/
│   ├── customers.csv                  # 5 000 klientów, 21 kolumn
│   ├── transactions.csv               # ~25 000 rekordów zakupów
│   ├── data_dictionary.md             # Opis kolumn i znane problemy jakości danych
│   └── checkpoints/                   # Bazowe punkty kontrolne (patrz niżej)
├── 3. notatniki/
│   ├── mp1_starter.ipynb — mp5_starter.ipynb  # Twoje notatniki robocze
│   └── skrypty/
│       └── verify_checkpoint.py       # Weryfikacja wyniku MP2 względem bazowego punktu kontrolnego
```

## Jak zacząć

1. Przeczytaj `1. projekt/1. scenariusz_biznesowy.md`, aby poznać kontekst
2. Skonfiguruj środowisko zgodnie z `1. projekt/3. konfiguracja_srodowiska.md` (zalecany Google Colab)
3. Otwórz `3. notatniki/mp1_starter.ipynb` i postępuj zgodnie z instrukcjami
4. Przed każdym MP przeczytaj odpowiedni opis (`1. projekt/mpN_opis.md`) oraz zajrzyj do `2. data/data_dictionary.md`

## Postęp mini-projektów

| MP | Tytuł | Co robisz |
|----|-------|-----------|
| MP1 | Kontekst biznesowy i eksploracja danych | Załaduj dane, zbadaj rozkłady, znajdź problemy jakości, wytrenuj baseline |
| MP2 | Czyszczenie danych i feature engineering | Parsuj daty, czyść ciągi tekstowe, obsłuż brakujące wartości, usuń wartości odstające, zakoduj, przeskaluj |
| MP3 | Modelowanie baseline i porównanie algorytmów | Wytrenuj Logistic Regression i Random Forest, oceń za pomocą krzywych ROC |
| MP4 | Ewaluacja modelu i wpływ biznesowy | Zbuduj cost matrix, oblicz zysk z kampanii, zoptymalizuj threshold |
| MP5 | Porównanie modeli i końcowa rekomendacja | Porównaj modele pod kątem zysku, fairness, interpretowalności; napisz rekomendację |

Każdy MP opiera się na poprzednim. Zapisz checkpoint na końcu każdego MP — następny notatnik go wczytuje.

## Zostajesz w tyle?

Bazowe punkty kontrolne w `2. data/checkpoints/` pozwalają rozpocząć dowolny MP bez ukończenia poprzednich. Instrukcje wczytywania znajdziesz w `2. data/checkpoints/README.md`.

## Reprodukowalność

Wszyscy studenci muszą uzyskać **identyczne wyniki liczbowe** (odpowiedzi w testach MCQ zależą od dokładnych wartości):
- Użyj `random_state=42` wszędzie
- Użyj scikit-learn 1.4-1.5, pandas 2.x, numpy <2.0
- Postępuj zgodnie z dokładną kolejnością przetwarzania z opisu MP2

Jeśli Twoje wyniki MP2 nie zgadzają się, uruchom `3. notatniki/skrypty/verify_checkpoint.py`, aby dowiedzieć się dlaczego.

## Ocenianie

5 mini-projektów × 10 pytań MCQ = **50 pytań łącznie**, dostępnych przez Edux w oknie 48 godzin, z 3 próbami na test. Szczegóły w `1. projekt/2. opis_projektu.md`.
