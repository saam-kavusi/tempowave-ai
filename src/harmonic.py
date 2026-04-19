"""Camelot wheel harmonic compatibility scoring."""


def _parse_camelot(key: str):
    """
    Parse a Camelot key string (e.g. '8B', '3A', '12B') into (number, letter).
    Returns None if the string is empty or malformed.
    """
    key = key.strip()
    if not key or len(key) < 2:
        return None
    try:
        number = int(key[:-1])
        letter = key[-1].upper()
        if letter not in ("A", "B") or not (1 <= number <= 12):
            return None
        return number, letter
    except ValueError:
        return None


def camelot_score(key1: str, key2: str) -> float:
    """
    Return a harmonic compatibility score in [0.0, 1.0] for two Camelot keys.

    Scoring tiers:
    - Same key (e.g. 8B → 8B):                           1.0  (perfect)
    - Adjacent number, same mode (e.g. 8B → 9B or 7B):   0.8  (strong)
    - Same number, opposite mode (e.g. 8A ↔ 8B):          0.8  (relative major/minor)
    - Two steps, same mode (e.g. 8B → 10B):               0.5  (moderate)
    - All other combinations:                              0.1  (weak / avoid)

    Falls back to 0.1 if either key is empty or unparseable.
    """
    parsed1 = _parse_camelot(key1)
    parsed2 = _parse_camelot(key2)

    if parsed1 is None or parsed2 is None:
        return 0.1

    n1, l1 = parsed1
    n2, l2 = parsed2

    # Circular distance on the 12-position Camelot wheel
    diff = abs(n1 - n2)
    circular_diff = min(diff, 12 - diff)

    if circular_diff == 0 and l1 == l2:
        return 1.0  # exact same key

    if (circular_diff == 1 and l1 == l2) or (circular_diff == 0 and l1 != l2):
        return 0.8  # adjacent number same mode, or relative major/minor

    if circular_diff == 2 and l1 == l2:
        return 0.5  # two steps same mode

    return 0.1  # incompatible
