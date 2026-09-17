import shutil
from datetime import datetime
from pathlib import Path

def fazer_backup(origem, destino, extensoes="", simular=True, logger=print):
    origem = Path(origem)
    destino = Path(destino)

    if not origem.exists():
        raise FileNotFoundError("A pasta de origem informada nao foi encontrada.")

    lista_ext = [e.strip().lower() for e in extensoes.split(",") if e.strip()]

    copiados = 0
    ignorados = 0

    for arquivo in origem.rglob("*"):
        if not arquivo.is_file():
            continue
        if lista_ext and arquivo.suffix.lower() not in lista_ext:
            ignorados += 1
            continue
        alvo = destino / arquivo.relative_to(origem)
        if alvo.exists() and alvo.stat().st_mtime >= arquivo.stat().st_mtime:
            logger(f"[SEM MUDANCA] {arquivo.name}")
            ignorados += 1
            continue
        if simular:
            logger(f"[SIMULACAO] copiaria {arquivo.name}")
        else:
            alvo.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(arquivo, alvo)
            logger(f"[COPIADO] {arquivo.name}")
        copiados += 1

    logger(f"Backup concluido: {copiados} copiado(s), {ignorados} ignorado(s).")
    return {"copiados": copiados, "ignorados": ignorados}