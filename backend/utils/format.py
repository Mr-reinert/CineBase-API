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

def formatar_dados_tmdb(dados):
    return {
        "id": dados.get("id"),
        "title": dados.get("title"),
        "overview": dados.get("overview"),
        "poster_url": dados.get("poster_path"),
        "release_date": dados.get("release_date"),
        "budget": dados.get("budget")
    }