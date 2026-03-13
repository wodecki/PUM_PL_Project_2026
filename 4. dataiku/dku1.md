# MP1 w Dataiku: Kontekst biznesowy i eksploracja danych (Bez kodowania)

**Cel:** Załadowanie danych MajsterPlus do Dataiku, zrozumienie ich struktury, zidentyfikowanie problemów jakościowych, wizualizacja rozkładów oraz stworzenie wizualnego modelu bazowego (baseline).

## Krok 1: Utworzenie projektu i wgranie danych

Zamiast pisać kod ładujący pliki CSV, w Dataiku używamy interfejsu wizualnego.

1. Zaloguj się do Dataiku i na stronie głównej kliknij **+ New Project** -> **Blank Project**. Nazwij go np. `MajsterPlus_Churn`.
2. Otwórz projekt i przejdź do zakładki **Flow** (przepływ pracy).
3. Kliknij **+ Import Your First Dataset** (lub wybierz z górnego menu `+ Dataset` -> `Upload your files`).
4. Przeciągnij i upuść plik `customers.csv`.
5. W oknie podglądu upewnij się, że dane wyświetlają się poprawnie (Dataiku zazwyczaj automatycznie wykrywa separator `,`). Nazwij dataset `customers_raw` i kliknij **Create**.
6. Powtórz kroki 3-5 dla pliku `transactions.csv` (nazwij go `transactions_raw`).

## Krok 2: Eksploracja danych i identyfikacja problemów (Data Understanding)

Zamiast funkcji `df.info()` czy `df.describe()` w Pythonie, Dataiku posiada potężną zakładkę **Explore**.

1. Otwórz zbiór `customers_raw`. Zwróć uwagę na pasek jakości pod nazwami kolumn (zielony = ok, czerwony = błąd, szary = brak danych).
2. **Analiza braków i typów:** Kliknij nagłówek dowolnej kolumny (np. `monthly_income_bracket`) i z rozwijanego menu wybierz **Analyze**. Otworzy się okno, w którym Dataiku podsumuje rozkład wartości, liczbę braków (Empty/Null) oraz wartości unikalne.
3. **Zidentyfikuj problemy jakościowe (Twoje zadanie):** Przejrzyj kolumny i znajdź "haczyki" przygotowane w słowniku danych:
   - Spójrz na kolumnę `total_spend`. Zobaczysz, że Dataiku wykryło ją jako tekst (String), ponieważ zawiera wartości typu `"PLN 1,496.76"`.
   - Spójrz na daty (`registration_date`). Zobaczysz, że są traktowane jako tekst przez polskie nazwy miesięcy (np. "21-kwi-2022").
   - *(Nie naprawiaj ich teraz! Czyszczenie to zadanie na etap MP2, w którym użyjecie narzędzia "Prepare recipe").*

## Krok 3: Wizualizacja rozkładów  i zbalansowania klas (Charts)

**1. Zbalansowanie klas i rozkłady zmiennych (Narzędzie Analyze):** Zamiast budować wykresy od zera, użyjemy wbudowanego profilowania danych.

- Będąc w widoku tabeli danych (zakładka **Explore**), znajdź kolumnę `is_lapsed`.
- Kliknij w jej nagłówek (lub w małą strzałkę obok nazwy) i z rozwijanego menu wybierz **Analyze**.
- Otworzy się okno podsumowania. Zobaczysz w nim dokładny histogram pokazujący, ile rekordów ma wartość `0` (aktywni), a ile `1` (churn). To idealnie obrazuje problem niezbalansowanych klas (~18% odejść).
- Powtórz tę samą czynność (kliknij **Analyze**) dla kolumn `age` oraz `satisfaction_score`. Dataiku automatycznie wygeneruje histogramy pokazujące wiek klientów i rozkład ich ocen.

**2. Wykrywanie wartości odstających - Outlierów (Zakładka Charts):** Aby wykryć anomalie w średniej wartości koszyka, musimy zbudować wykres pudełkowy.

- Przejdź do zakładki **Charts** (w lewym górnym rogu).
- Kliknij ikonę wyboru wykresu. Z menu przejdź do sekcji **Others** (na samym dole) i wybierz **Boxplot**.
- Przeciągnij kolumnę `avg_basket_value` do pola **Y**.
- Wykres wygeneruje pudełko z "wąsami". Zobaczysz pojedyncze kropki uciekające daleko w górę poza główny rozkład – to są właśnie skrajne wartości odstające (outliery), którymi zajmiesz się w MP2.

## Krok 4: Zależności i korelacje (Statistics)

W Pythonie użylibyśmy mapy cieplnej (Correlation Heatmap). W Dataiku mamy na to dedykowaną kartę.

**WAŻNE:** dla zmiennych numerycznych, których korelacje chcesz obliczyć, musisz wcześniej zmienić typ:
w widoku Explore wybierz kolumnę danej zmiennej (np. `age`) i zmień jej typ (wiersz zaraz pod nazwą) ze `string` na np. `int`. Jeśli tego nie zrobisz, Dataiku potraktuje tę zmienną jako kategorialną.

1. Będąc w zbiorze `customers_raw`, przejdź do zakładki **Statistics**.
2. Kliknij **+ Create your first worksheet** -> wybierz **Multivariate Aanlysis** * > *Correlation Matrix**.
3. Wybierz zmienne numeryczne (np. `age`, `purchase_count`, `avg_basket_value`, `is_lapsed`, `satisfaction_score`).
4. Kliknij **Compute**. Dataiku wygeneruje interaktywną mapę cieplną. Zbadaj, które zmienne wydają się najsilniej skorelowane ze zmienną `is_lapsed`.

## Krok 5: Szybki model Baseline (AutoML / Visual ML)

To najbardziej ekscytująca część. Stworzymy pierwszy model bazowy bez pisania kodu.

1. Wróć do zakładki **Explore** dla zbioru `customers_raw`.
2. Kliknij prawym przyciskiem myszy na nagłówek kolumny `is_lapsed` i wybierz **Create Prediction Model** (lub kliknij przycisk **Lab** w prawym górnym rogu -> *AutoML Prediction* -> wybierz `is_lapsed`).
3. Wybierz szablon **Quick Prototypes** i kliknij **Create**.
4. **UWAGA BIZNESOWA (BARDZO WAŻNE):** Przejdź do zakładki **Design** w panelu modelu, a następnie do sekcji **Features**.
   - Znajdź zmienną `days_since_last_purchase` i **wyłącz ją** (odznacz suwak). Dlaczego? Zgodnie z instrukcją, ta zmienna w 100% determinuje odejście klienta (>90 dni). Użycie jej to tzw. *data leakage* (wyciek danych).
5. Przejdź do sekcji **Algorithms**. Dataiku domyślnie wybierze np. Random Forest i Logistic Regression. Pozostaw je.
6. Kliknij zielony przycisk **TRAIN** (w prawym górnym rogu).
7. Po chwili Dataiku wyświetli wyniki. Kliknij na najlepszy model, aby wejść w jego szczegóły.
8. Przejdź do zakładki **Performance** -> **ROC curve**, aby zobaczyć pole pod krzywą (ROC-AUC). Oczekiwany wynik dla baseline to około ~0.83.
9. Przejdź do zakładki **Explainability** -> **Variables Importance**, aby zobaczyć, które cechy (na tym wczesnym etapie) model uznał za najważniejsze.

## Krok 6: Podsumowanie obserwacji (Raportowanie)

W Dataiku możesz stworzyć wizualny Dashboard, aby odpowiedzieć na pytania z oryginalnego notatnika.

1. Przejdź do menu głównego projektu i wybierz **Dashboards**.
2. Utwórz nowy Dashboard. Możesz do niego "przypiąć" (używając ikony pinezki) wcześniej stworzone wykresy z zakładki *Charts*, macierz korelacji, a także wyniki modelu ROC-AUC z sekcji *Lab*.
3. Dodaj kafelki tekstowe (Text insight), w których jako zespół odpowiecie na 5 pytań kontrolnych z etapu 1 (m.in. dlaczego wysokie *accuracy* jest mylące przy 18% churnie, i jakie problemy jakościowe zostały zauważone).