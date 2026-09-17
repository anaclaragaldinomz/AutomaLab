import os
import shutil
from pathlib import Path

CATEGORIAS = {
    "imagens":     [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
    "documentos":  [".pdf", ".doc", ".docx", ".txt", ".odt", ".xls", ".xlsx", ".ppt", ".pptx"],
    "videos":      [".mp4", ".avi", ".mkv", ".mov"],
    "musicas":     [".mp3", ".wav", ".flac"],
    "compactados": [".zip", ".rar", ".7z", ".tar", ".gz"],
}

def classificar(nome_arquivo):
    extensao = Path(nome_arquivo).suffix.lower()
    for categoria, extensoes in CATEGORIAS.items():
        if extensao in extensoes:
            return categoria
    return "outros"

def organizar(origem, destino, modo="mover", simular=True, logger=print):
    origem = Path(origem)
    destino = Path(destino)

    if not origem.exists():
        raise FileNotFoundError(f"Pasta de origem inexistente: {origem}")

    arquivos = [a for a in origem.iterdir() if a.is_file()]

    if not arquivos:
        logger("Nenhum arquivo encontrado para organizar.")
        return {"total": 0, "por_categoria": {}}

    contagem = {}

    for arquivo in arquivos:                              
        categoria = classificar(arquivo.name)             

        if categoria == "outros" and modo == "manter":   
            logger(f"[IGNORADO] {arquivo.name} (sem categoria definida)")
            continue

        pasta_categoria = destino / categoria
        destino_final = pasta_categoria / arquivo.name

        if simular:                                      
            logger(f"[SIMULAÇÃO] {arquivo.name} -> {categoria}/")
        else:
            pasta_categoria.mkdir(parents=True, exist_ok=True)
            shutil.move(str(arquivo), str(destino_final))
            logger(f"[MOVIDO] {arquivo.name} -> {categoria}/")

        contagem[categoria] = contagem.get(categoria, 0) + 1

    logger("Organização concluída.")
    return {"total": sum(contagem.values()), "por_categoria": contagem}

if __name__ == "__main__":
    resultado = organizar(
        origem="C:\AutomaLabTeste\origem",
        destino="C:\AutomaLabTeste\organizado",
        modo="mover",
        simular=True,
    )
    print("Resumo:", resultado)