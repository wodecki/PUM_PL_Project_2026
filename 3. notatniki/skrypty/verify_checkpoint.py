#!/usr/bin/env python3
# /// script
# dependencies = [
#     "pandas>=2.0,<3.0",
#     "numpy>=1.26,<2.0",
#     "scikit-learn>=1.4,<1.6",
# ]
# requires-python = ">=3.10"
# ///
"""Weryfikacja wyniku MP2 studenta względem bazowego punktu kontrolnego.

Porównuje przetworzony DataFrame studenta z bazowym checkpoint_for_mp3,
wyświetlając konkretne, praktyczne komunikaty o błędach dla każdej niezgodności.

Użycie:
    uv run "3. notatniki/skrypty/verify_checkpoint.py" <student_checkpoint.pkl>

    Jeśli nie podano argumentu, sprawdza wewnętrzny checkpoint w checkpoints/mp2_checkpoint.pkl.
"""

import pickle
import sys
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
GOLDEN_DIR = PROJECT_ROOT / "2. data" / "checkpoints"


class CheckResult:
    def __init__(self):
        self.passed = 0
        self.failed = 0

    def check(self, name: str, condition: bool, detail: str = ""):
        if condition:
            self.passed += 1
            print(f"  \u2705 {name}")
        else:
            self.failed += 1
            msg = f"  \u274c {name}"
            if detail:
                msg += f"\n     → {detail}"
            print(msg)

    def summary(self) -> bool:
        total = self.passed + self.failed
        print(f"\n{'=' * 60}")
        print(f"  {self.passed}/{total} sprawdzeń zaliczonych")
        if self.failed > 0:
            print(f"  Znaleziono {self.failed} problemów — szczegóły powyżej")
        else:
            print("  Twój checkpoint zgadza się z bazowym punktem kontrolnym!")
        print(f"{'=' * 60}")
        return self.failed == 0


def main():
    # Określ ścieżkę checkpointu studenta
    if len(sys.argv) > 1:
        student_path = Path(sys.argv[1])
    else:
        student_path = PROJECT_ROOT / "checkpoints" / "mp2_checkpoint.pkl"

    golden_path = GOLDEN_DIR / "checkpoint_for_mp3.pkl"

    if not golden_path.exists():
        print(f"BŁĄD: Nie znaleziono bazowego checkpointu w {golden_path}")
        print("Uruchom: uv run scripts/build_checkpoints.py")
        sys.exit(1)

    if not student_path.exists():
        print(f"BŁĄD: Nie znaleziono checkpointu studenta w {student_path}")
        print("Najpierw uruchom swój notatnik z rozwiązaniem MP2, aby wygenerować checkpoint.")
        sys.exit(1)

    print("=" * 60)
    print("Weryfikacja checkpointu: Student vs bazowy punkt kontrolny")
    print("=" * 60)
    print(f"  Student:  {student_path}")
    print(f"  Bazowy:   {golden_path}")
    print()

    with open(golden_path, "rb") as f:
        golden = pickle.load(f)
    with open(student_path, "rb") as f:
        student = pickle.load(f)

    v = CheckResult()

    # Sprawdź klucze
    golden_keys = set(golden.keys())
    student_keys = set(student.keys())
    missing_keys = golden_keys - student_keys
    v.check(
        "Checkpoint zawiera wymagane klucze",
        len(missing_keys) == 0,
        f"Brakujące klucze: {missing_keys}. Twój checkpoint powinien zawierać: {sorted(golden_keys)}"
    )

    # Sprawdź kształt X_train
    if "X_train" in student:
        g_shape = golden["X_train"].shape
        s_shape = student["X_train"].shape
        v.check(
            f"Kształt X_train zgadza się ({g_shape})",
            s_shape == g_shape,
            f"Twój X_train ma kształt {s_shape}, oczekiwano {g_shape}. "
            + (f"Niezgodność wierszy: sprawdź krok usuwania wartości odstających (IQR na avg_basket_value). "
               if s_shape[0] != g_shape[0] else "")
            + (f"Niezgodność kolumn: sprawdź krok kodowania (one-hot + ordinal). "
               f"Oczekiwano {g_shape[1]} cech po kodowaniu."
               if len(s_shape) > 1 and len(g_shape) > 1 and s_shape[1] != g_shape[1] else "")
        )

    # Sprawdź kształt X_test
    if "X_test" in student:
        g_shape = golden["X_test"].shape
        s_shape = student["X_test"].shape
        v.check(
            f"Kształt X_test zgadza się ({g_shape})",
            s_shape == g_shape,
            f"Twój X_test ma kształt {s_shape}, oczekiwano {g_shape}."
        )

    # Sprawdź y_train
    if "y_train" in student:
        g_len = len(golden["y_train"])
        s_len = len(student["y_train"])
        v.check(
            f"Długość y_train zgadza się ({g_len})",
            s_len == g_len,
            f"Twój y_train ma {s_len} próbek, oczekiwano {g_len}. "
            "Sprawdź, czy usunąłeś te same wiersze z wartościami odstającymi zarówno z X, jak i z y."
        )

        g_rate = golden["y_train"].mean()
        s_rate = student["y_train"].mean()
        v.check(
            f"Wskaźnik odejść y_train zgadza się ({g_rate:.3f})",
            abs(s_rate - g_rate) < 0.01,
            f"Twój wskaźnik odejść y_train wynosi {s_rate:.3f}, oczekiwano {g_rate:.3f}. "
            "Sprawdź stratified split: train_test_split(..., stratify=y)."
        )

    # Sprawdź y_test
    if "y_test" in student:
        g_rate = golden["y_test"].mean()
        s_rate = student["y_test"].mean()
        v.check(
            f"Wskaźnik odejść y_test zgadza się ({g_rate:.3f})",
            abs(s_rate - g_rate) < 0.01,
            f"Twój wskaźnik odejść y_test wynosi {s_rate:.3f}, oczekiwano {g_rate:.3f}."
        )

    # Sprawdź nazwy cech
    if "feature_names" in student and "feature_names" in golden:
        g_feats = sorted(golden["feature_names"])
        s_feats = sorted(student["feature_names"])
        v.check(
            f"Nazwy cech zgadzają się ({len(g_feats)} cech)",
            g_feats == s_feats,
            _feature_diff_detail(g_feats, s_feats)
        )

    # Sprawdź kolejność kolumn (posortowane alfabetycznie)
    if "X_train" in student and hasattr(student["X_train"], "columns"):
        g_cols = list(golden["X_train"].columns)
        s_cols = list(student["X_train"].columns)
        v.check(
            "Kolejność kolumn zgadza się (posortowane alfabetycznie)",
            g_cols == s_cols,
            f"Pierwsza różnica na pozycji {_first_diff(g_cols, s_cols)}. "
            "Czy posortowałeś kolumny alfabetycznie? df = df[sorted(df.columns)]"
            if g_cols != s_cols else ""
        )

    # Sprawdź wartości null
    if "X_train" in student and hasattr(student["X_train"], "isnull"):
        s_nulls = student["X_train"].isnull().sum().sum()
        v.check(
            "X_train nie ma wartości null",
            s_nulls == 0,
            f"Twój X_train ma {s_nulls} wartości null. "
            "Sprawdź kroki imputation (mediana dla numerycznych, moda dla kategorycznych)."
        )

    # Sprawdź skalowanie (średnie bliskie 0, odchylenia bliskie 1) — z wyłączeniem kolumny cluster
    if "X_train" in student and hasattr(student["X_train"], "mean"):
        cols_to_check = [c for c in student["X_train"].columns if c != "cluster"]
        means = student["X_train"][cols_to_check].mean()
        max_mean = means.abs().max()
        v.check(
            "X_train wygląda na przeskalowany (średnie ≈ 0, z wyłączeniem cluster)",
            max_mean < 0.1,
            f"Maks. średnia kolumny = {max_mean:.4f}. "
            "Czy zastosowałeś StandardScaler? Dopasuj na train, transformuj zarówno train, jak i test."
        )

    # Sprawdź przybliżoną zgodność wartości liczbowych (pierwsze kilka wierszy)
    if "X_train" in student and "X_train" in golden:
        try:
            g_vals = golden["X_train"].values[:5, :5].flatten()
            s_vals = student["X_train"].values[:5, :5].flatten()
            if len(g_vals) == len(s_vals):
                max_diff = np.max(np.abs(g_vals - s_vals))
                v.check(
                    "Wartości liczbowe w przybliżeniu się zgadzają (pierwszy blok 5×5)",
                    max_diff < 0.01,
                    f"Maks. różnica = {max_diff:.6f}. "
                    "Wartości powinny się zgadzać, jeśli kroki przetwarzania wykonano w prawidłowej kolejności."
                )
        except Exception:
            pass

    v.summary()
    sys.exit(0 if v.failed == 0 else 1)


def _feature_diff_detail(golden: list, student: list) -> str:
    g_set = set(golden)
    s_set = set(student)
    missing = g_set - s_set
    extra = s_set - g_set
    parts = []
    if missing:
        parts.append(f"Brakujące cechy: {sorted(missing)}")
    if extra:
        parts.append(f"Dodatkowe cechy: {sorted(extra)}")
    if not parts:
        parts.append("Te same cechy, ale inna kolejność")
    return " | ".join(parts)


def _first_diff(a: list, b: list) -> int:
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            return i
    return min(len(a), len(b))


if __name__ == "__main__":
    main()
