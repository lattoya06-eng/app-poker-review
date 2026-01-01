def make_decision(pot_odds, estimated_equity):
    if estimated_equity >= pot_odds:
        return "CALL aceitável"
    else:
        return "FOLD recomendado"
