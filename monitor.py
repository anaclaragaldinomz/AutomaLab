import shutil
import subprocess
from datetime import datetime

def _memoria_psutil():
    import psutil
    m = psutil.virtual_memory()
    return round(m.total / 1024**3, 2), round(m.used / 1024**3, 2), round(m.percent, 1)

def _memoria_wmic():
    saida = subprocess.run(
        ["wmic", "OS", "get", "FreePhysicalMemory,TotalVisibleMemorySize", "/Value"],
        capture_output=True, text=True,
    ).stdout
    valores = {}
    for linha in saida.splitlines():
        if "=" in linha:
            chave, valor = linha.split("=", 1)
            valores[chave.strip()] = valor.strip()
    total = int(valores.get("TotalVisibleMemorySize", 0)) / 1024**2
    livre = int(valores.get("FreePhysicalMemory", 0)) / 1024**2
    usado = total - livre
    percentual = (usado / total * 100) if total else 0
    return round(total, 2), round(usado, 2), round(percentual, 1)

def _processos(limite=8):
    try:
        import psutil
        lista = []
        for p in psutil.process_iter(["name", "memory_percent"]):
            try:
                lista.append((p.info["name"], p.info["memory_percent"] or 0))
            except Exception:
                pass
        lista.sort(key=lambda x: x[1], reverse=True)
        return [f"{nome} ({pct:.1f}% mem)" for nome, pct in lista[:limite]]
    except ImportError:
        saida = subprocess.run(
            ["tasklist", "/FO", "CSV", "/NH"], capture_output=True, text=True
        ).stdout
        nomes = []
        for linha in saida.splitlines()[:limite]:
            partes = linha.split('","')
            if partes:
                nomes.append(partes[0].strip('"'))
        return nomes

def monitorar(caminho_disco="C:/", logger=print):
    linha = "-" * 50

    try:
        uso = shutil.disk_usage(caminho_disco)
        logger(linha)
        logger("DISCO")
        logger(f"Total: {uso.total / 1024**3:.1f} GB")
        logger(f"Livre: {uso.free / 1024**3:.1f} GB")
        logger(f"Usado: {uso.used / uso.total * 100:.1f}%")
    except Exception:
        logger("Nao foi possivel ler o disco informado.")

    try:
        total, usado, pct = _memoria_psutil()
    except ImportError:
        total, usado, pct = _memoria_wmic()

    logger(linha)
    logger("MEMORIA")
    logger(f"Total: {total} GB")
    logger(f"Usado: {usado} GB ({pct}%)")

    logger(linha)
    logger("PROCESSOS MAIS PESADOS")
    for nome in _processos():
        logger(f"- {nome}")

    logger(linha)
    logger("Relatorio gerado.")
    return {"relatorio": True}