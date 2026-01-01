def estimate_equity(hand_strength):
    if hand_strength == "forte":
        return 0.45
    elif hand_strength == "media":
        return 0.30
    else:
        return 0.15
