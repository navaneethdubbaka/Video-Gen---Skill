#!/usr/bin/env python3
"""Romanize Telugu script to Latin letters (phonetic English spellings).

Keeps already-Latin tokens unchanged. For short-form captions when VO is Telugu.
"""

from __future__ import annotations

import re
import unicodedata

IND_VOWELS = {
    "\u0c05": "a",
    "\u0c06": "aa",
    "\u0c07": "i",
    "\u0c08": "ee",
    "\u0c09": "u",
    "\u0c0a": "oo",
    "\u0c0b": "ru",
    "\u0c60": "ruu",
    "\u0c0e": "e",
    "\u0c0f": "e",
    "\u0c10": "ai",
    "\u0c12": "o",
    "\u0c13": "o",
    "\u0c14": "au",
}

CONSONANTS = {
    "\u0c15": "k",
    "\u0c16": "kh",
    "\u0c17": "g",
    "\u0c18": "gh",
    "\u0c19": "ng",
    "\u0c1a": "ch",
    "\u0c1b": "chh",
    "\u0c1c": "j",
    "\u0c1d": "jh",
    "\u0c1e": "ny",
    "\u0c1f": "t",
    "\u0c20": "th",
    "\u0c21": "d",
    "\u0c22": "dh",
    "\u0c23": "n",
    "\u0c24": "t",
    "\u0c25": "th",
    "\u0c26": "d",
    "\u0c27": "dh",
    "\u0c28": "n",
    "\u0c2a": "p",
    "\u0c2b": "ph",
    "\u0c2c": "b",
    "\u0c2d": "bh",
    "\u0c2e": "m",
    "\u0c2f": "y",
    "\u0c30": "r",
    "\u0c31": "r",
    "\u0c32": "l",
    "\u0c33": "l",
    "\u0c35": "v",
    "\u0c36": "sh",
    "\u0c37": "sh",
    "\u0c38": "s",
    "\u0c39": "h",
}

MATRAS = {
    "\u0c3e": "aa",
    "\u0c3f": "i",
    "\u0c40": "ee",
    "\u0c41": "u",
    "\u0c42": "oo",
    "\u0c43": "ru",
    "\u0c44": "ruu",
    "\u0c46": "e",
    "\u0c47": "e",
    "\u0c48": "ai",
    "\u0c4a": "o",
    "\u0c4b": "o",
    "\u0c4c": "au",
}

VIRAMA = "\u0c4d"
ANUSVARA = "\u0c02"
VISARGA = "\u0c03"


def has_telugu(text: str) -> bool:
    return any("\u0c00" <= ch <= "\u0c7f" for ch in text)


_EDGE = set(" \t\n\r.,!?;:'\"()[]{}<>\"-_/\\|@#$%^&*+=~`")


def _split_edges(word: str) -> tuple[str, str, str]:
    # Strip ASCII punctuation only. Telugu matras are Mn and must stay in core.
    i = 0
    j = len(word)
    while i < j and word[i] in _EDGE:
        i += 1
    while j > i and word[j - 1] in _EDGE:
        j -= 1
    return word[:i], word[i:j], word[j:]


def romanize_telugu_word(word: str) -> str:
    if not word or not has_telugu(word):
        return word

    pre, core, post = _split_edges(word)
    if not core or not has_telugu(core):
        return word

    out: list[str] = []
    chars = list(core)
    i = 0
    n = len(chars)

    while i < n:
        ch = chars[i]

        if ch in IND_VOWELS:
            out.append(IND_VOWELS[ch])
            i += 1
            continue

        if ch in CONSONANTS:
            base = CONSONANTS[ch]
            i += 1
            if i < n and chars[i] == VIRAMA:
                i += 1
                out.append(base)
                continue
            if i < n and chars[i] in MATRAS:
                out.append(base + MATRAS[chars[i]])
                i += 1
                continue
            if i < n and chars[i] == ANUSVARA:
                nxt = chars[i + 1] if i + 1 < n else ""
                out.append(base + ("an" if nxt in CONSONANTS else "am"))
                i += 1
                continue
            if i < n and chars[i] == VISARGA:
                out.append(base + "ah")
                i += 1
                continue
            out.append(base + "a")
            continue

        if ch == VIRAMA:
            i += 1
            continue
        if ch == ANUSVARA:
            # Before a consonant, nasalize as "n" (caption-friendly); else "m".
            nxt = chars[i + 1] if i + 1 < n else ""
            out.append("n" if nxt in CONSONANTS else "m")
            i += 1
            continue
        if ch == VISARGA:
            out.append("h")
            i += 1
            continue
        if ch in MATRAS:
            out.append(MATRAS[ch])
            i += 1
            continue
        if "\u0c00" <= ch <= "\u0c7f":
            name = unicodedata.name(ch, "")
            if "VIRAMA" in name or "SIGN" in name:
                i += 1
                continue
            out.append(ch)
            i += 1
            continue

        out.append(ch)
        i += 1

    roman = "".join(out)
    roman = re.sub(r"aa+", "aa", roman)
    return f"{pre}{roman}{post}"


def romanize_text(text: str) -> str:
    if not text or not has_telugu(text):
        return text
    parts = re.split(r"(\s+)", text)
    return "".join(romanize_telugu_word(p) if not p.isspace() else p for p in parts)


if __name__ == "__main__":
    samples = [
        "\u0c05\u0c28\u0c47",
        "\u0c15\u0c4a\u0c24\u0c4d\u0c24",
        "\u0c1a\u0c47\u0c38\u0c3f\u0c02\u0c26\u0c3f.",
        "Recently Swiggy \u0c05\u0c28\u0c47 \u0c15\u0c4a\u0c24\u0c4d\u0c24 feature",
    ]
    for s in samples:
        print(f"{s!r} -> {romanize_text(s)!r}")

