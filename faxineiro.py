from datetime import datetime, timedelta
from pathlib import Path

def limpar(pasta, dias_antigos=30, extensoes="", simular=True, logger=print):
    pasta = Path(pasta)

    if not pasta.exists():
        raise FileNotFoundError("A pasta informada nao foi encontrada.")
    if "AutomaLabTeste" not in str(pasta):
        raise PermissionError(
            "Por seguranca, a limpeza so roda dentro de C:\AutomaLabTeste."
        )

    limite = datetime.now() - timedelta(days=dias_antigos)
    lista_ext = [e.strip().lower() for e in extensoes.split(",") if e.strip()]

    apagados = 0
    espaco = 0

    for arquivo in pasta.rglob("*"):
        if not arquivo.is_file():
            continue
        if lista_ext and arquivo.suffix.lower() not in lista_ext:
            continue
        modificado = datetime.fromtimestamp(arquivo.stat().st_mtime)
        if modificado >= limite:
            continue
        tamanho = arquivo.stat().st_size
        if simular:
            logger(f"[SIMULACAO] apagaria {arquivo.name}")
        else:
            arquivo.unlink()
            logger(f"[APAGADO] {arquivo.name}")
        apagados += 1
        espaco += tamanho

    logger(f"Limpeza concluida: {apagados} arquivo(s), {espaco / 1024:.1f} KB liberados.")
    return {"apagados": apagados, "kb_liberados": round(espaco / 1024, 1)}