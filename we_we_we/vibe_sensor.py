from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from typing import Dict, List, Tuple


PAPIAMENTU_SUGAR_WORDS = {
    "dushi",
    "ayó",
    "bon",
    "bini",
    "kon",
    "bo",
    "ta",
    "kla",
    "plase",
    "sinti",
    "jajajaja",
    "mmm",
    "mmmm",
    "we",
}

_RE_KEYSMASH = re.compile(r"[a-z]{3,}", re.IGNORECASE)
_RE_REPEATING_CHAR = re.compile(r"(.)\1{2,}")
_RE_REPEATING_PUNCT = re.compile(r"([!?\.])\1{2,}")


@dataclass
class VibeReport:
    """Light-weight container with analysis metrics."""

    length: int
    word_count: int
    repetition_rate: float
    keysmash_hits: int
    punct_overload: int
    sugar_hits: int
    palindrome_hits: int

    def glitch_score(self) -> float:
        """Rough composite glitch indicator (0-1)."""
        score = 0.0
        score += min(self.repetition_rate, 1.0) * 0.25
        score += min(self.keysmash_hits / 5, 1.0) * 0.25
        score += min(self.punct_overload / 5, 1.0) * 0.25
        score += min(self.sugar_hits / 5, 1.0) * 0.25
        return round(score, 3)

    def comfort_index(self) -> float:
        """Return a 0-1 comfort metric based on palindromic tokens (soothing loops)."""
        return min(self.palindrome_hits / 3, 1.0)

    def to_dict(self) -> Dict[str, float | int]:
        d = self.__dict__.copy()
        d["glitch_score"] = self.glitch_score()
        d["comfort_index"] = self.comfort_index()
        return d


# ---------------------------------------------------------------------------
# public api
# ---------------------------------------------------------------------------

def analyze_text(text: str) -> VibeReport:
    """Analyze *text* and return a :class:`VibeReport`. Lightweight & offline."""

    words = re.findall(r"[\w']+", text.lower())
    word_count = len(words)

    repetition_rate = _calc_repetition_rate(words)
    keysmash_hits = len(_RE_REPEATING_CHAR.findall(text)) + len(_detect_keysmash(text))
    punct_overload = len(_RE_REPEATING_PUNCT.findall(text))
    sugar_hits = sum(1 for w in words if w in PAPIAMENTU_SUGAR_WORDS)
    palindrome_hits = sum(1 for w in words if len(w) > 2 and w == w[::-1])

    return VibeReport(
        length=len(text),
        word_count=word_count,
        repetition_rate=repetition_rate,
        keysmash_hits=keysmash_hits,
        punct_overload=punct_overload,
        sugar_hits=sugar_hits,
        palindrome_hits=palindrome_hits,
    )


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _calc_repetition_rate(words: List[str]) -> float:
    if not words:
        return 0.0
    counts = Counter(words)
    repeated_tokens = sum(c for c in counts.values() if c > 1)
    return repeated_tokens / len(words)


def _detect_keysmash(text: str) -> List[str]:
    # sequence of random letters that are not common english tokens length >=6
    candidates = _RE_KEYSMASH.findall(text.lower())
    filtered: List[str] = []
    for c in candidates:
        # skip if word appears in dictionary of sugar words or common english? simple filter length>6 & not vowels heavy
        if len(c) >= 6 and not c in PAPIAMENTU_SUGAR_WORDS:
            # heuristically filter typical keysmash patterns repeated substring sequences
            if re.search(r"sksk|asdf|dfgh|ghjk", c):
                filtered.append(c)
            elif len(set(c)) > 4 and any(ch.isalpha() for ch in c):
                filtered.append(c)
    return filtered