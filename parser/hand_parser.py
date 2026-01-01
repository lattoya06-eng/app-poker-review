import re


def extract_numbers(text):
    data = {
        "stack": None,
        "pot": None,
        "bet": None
    }

    clean = (
        text.lower()
        .replace(",", ".")
        .replace("\n", " ")
    )

    # -------------------------
    # 1️⃣ CAPTURAR TODOS OS NÚMEROS
    # -------------------------
    numbers = [float(n) for n in re.findall(r"\d+\.\d+|\d+", clean)]

    # -------------------------
    # 2️⃣ STACK (BB)
    # -------------------------
    stack_candidates = []

    for match in re.finditer(r"(\d+\.\d+|\d+)\s*bb", clean):
        value = float(match.group(1))
        if value > 5:
            stack_candidates.append(value)

    if stack_candidates:
        data["stack"] = max(stack_candidates)

    # -------------------------
    # 3️⃣ POT
    # -------------------------
    pot_candidates = []

    for match in re.finditer(r"pot\s*[:=]?\s*(\d+\.\d+|\d+)", clean):
        pot_candidates.append(float(match.group(1)))

    # fallback: número médio (heurística)
    if not pot_candidates:
        for n in numbers:
            if 2 <= n <= 50:
                pot_candidates.append(n)

    if pot_candidates:
        data["pot"] = max(pot_candidates)

    # -------------------------
    # 4️⃣ BET / ALL-IN
    # -------------------------
    bet_candidates = []

    for match in re.finditer(r"(bet|raise|all[-\s]?in)\s*(\d+\.\d+|\d+)", clean):
        bet_candidates.append(float(match.group(2)))

    # fallback: menor valor relevante
    if not bet_candidates and data["pot"]:
        for n in numbers:
            if n < data["pot"]:
                bet_candidates.append(n)

    if bet_candidates:
        data["bet"] = min(bet_candidates)

    return data
