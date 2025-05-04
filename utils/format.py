def formatar_duracao(minutos: int) -> str:
    if not minutos:
        return "N/A"
    horas = minutos // 60
    mins = minutos % 60
    return f"{horas}h {mins}min" if horas else f"{mins}min"

def formatar_dinheiro(valor: int) -> str:
    if not valor:
        return "N/A"
    if valor >= 1_000_000_000:
        return f"${valor/1_000_000_000:.1f}B"
    elif valor >= 1_000_000:
        return f"${valor/1_000_000:.1f}M"
    return f"${valor:,}"
